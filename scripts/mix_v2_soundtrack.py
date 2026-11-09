"""Add independently configurable theme music; copy approved video packets.

FFmpeg/FFprobe and Python standard library only. Never overwrite review media.
"""
import argparse
import array
import hashlib
import json
import math
import subprocess
from pathlib import Path


def run(args):
    return subprocess.check_output(args)


def ff(*args):
    return run(['ffmpeg', '-v', 'error', '-n', *map(str, args)])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(path)]))['streams']


def hashes(path):
    data=ff('-i', path, '-map', '0:v:0', '-an', '-f', 'framemd5', '-').decode()
    return [line.split(',')[-1].strip() for line in data.splitlines() if not line.startswith('#')]


def floats(path):
    return array.array('f', ff('-i', path, '-vn', '-ac', 2, '-ar', 48000, '-f', 'f32le', '-'))


def main(manifest):
    c=json.loads(Path(manifest).read_text())
    source=c['sourceVideo'];music=c['musicSource'];out=Path(c['output'])
    work=Path(c['workDir']);work.mkdir(parents=True,exist_ok=True)
    assert not out.exists(),out
    checksums={p:sha(p) for p in [source,music]}
    video=next(s for s in probe(source) if s['codec_type']=='video')
    assert (video['width'],video['height'],int(video['nb_frames']))==(1280,720,c['frames'])
    assert video['avg_frame_rate']==f"{c['fps']}/1"
    total=c['frames']/c['fps'];rate=c['sampleRate'];assert rate==48000
    audio=next(s for s in probe(music) if s['codec_type']=='audio')
    duration=int(audio['duration_ts'])*float(audio['time_base'].split('/')[0])/float(audio['time_base'].split('/')[1])
    overlap=c['loopCrossfadeSeconds'];assert 0<overlap<duration/2
    copies=max(1,1+math.ceil(max(0,total-duration)/(duration-overlap)))
    filters=[]
    if copies>1:
        filters.append(f"[0:a]asplit={copies}"+''.join(f'[m{i}]' for i in range(copies)))
        last='m0'
        for i in range(1,copies):
            filters.append(f'[{last}][m{i}]acrossfade=d={overlap}:c1=hsin:c2=hsin[loop{i}]')
            last=f'loop{i}'
    else:last='0:a'
    # Duck before incoming dialogue; raise only after leaving a dialogue scene.
    # Gains are relative to the original WAV, with short cubic ramps.
    scenes=c['scenes'];gains=c['musicGainDb'];ramp=c['sceneGainTransitionSeconds']
    assert scenes[0]['startFrame']==0 and scenes[-1]['endFrame']==c['frames']
    def gain(scene):return 10**(gains[scene['gain']]/20)
    expr=f'{gain(scenes[0]):.12f}'
    for previous,scene in zip(scenes,scenes[1:]):
        assert previous['endFrame']==scene['startFrame']
        boundary=scene['startFrame']/c['fps']
        if gain(scene)>gain(previous):start=boundary;end=boundary+ramp
        else:start=boundary-ramp;end=boundary
        u=f'((t-{start:.12f})/{ramp:.12f})'
        smooth=f'({u}*{u}*(3-2*{u}))'
        expr=f'if(lt(t,{start:.12f}),{expr},if(lt(t,{end:.12f}),{gain(previous):.12f}+({gain(scene)-gain(previous):.12f})*{smooth},{gain(scene):.12f}))'
    stem=work/'music-stem.wav'
    filters.append(f"[{last}]aresample={rate},atrim=duration={total:.12f},asetpts=PTS-STARTPTS,asetnsamples=n=128:p=0,volume='{expr}':eval=frame,afade=t=in:d={c['fadeInSeconds']},afade=t=out:st={total-c['fadeOutSeconds']:.12f}:d={c['fadeOutSeconds']}[music]")
    (work/'music-filter.txt').write_text(';'.join(filters)+'\n')
    ff('-i',music,'-filter_complex_script',work/'music-filter.txt','-map','[music]','-c:a','pcm_f32le',stem)
    raw=work/'mix-unlimited.wav'
    mix=f'[0:a]aresample={rate},apad,atrim=duration={total:.12f},asetpts=PTS-STARTPTS[dialogue];[dialogue][1:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,volume={c["masterGainDb"]}dB[mix]'
    ff('-i',source,'-i',stem,'-filter_complex',mix,'-map','[mix]','-c:a','pcm_f32le',raw)
    samples=floats(raw);peak=max(abs(x) for x in samples)
    original=floats(source);music_samples=floats(stem)
    master=10**(c['masterGainDb']/20)
    sum_error=max(abs(y-(x+m)*master) for x,m,y in zip(original,music_samples,samples))
    assert sum_error<1e-6, sum_error
    # Abort rather than silently attenuate the dialogue or clip the combined mix.
    # If headroom is insufficient, lower the music gain and review another mix.
    assert peak<1, f'Mix exceeds full scale ({peak}); lower music gain before encoding.'
    ff('-i',source,'-i',raw,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar',rate,'-movflags','+faststart',out)
    assert hashes(source)==hashes(out)
    ff('-i',out,'-f','null','-')
    assert checksums=={p:sha(p) for p in checksums}
    v=next(s for s in probe(out) if s['codec_type']=='video')
    assert int(v['nb_frames'])==c['frames'] and abs(float(v['duration'])-total)<.00001
    report={'output':str(out),'manifest':manifest,'inputSHA256':checksums,'sourcesUnchanged':True,'frames':c['frames'],'fps':c['fps'],'durationSeconds':total,'resolution':[1280,720],'allDecodedVideoFramesIdentical':True,'musicDurationSeconds':duration,'musicCopies':copies,'loopOverlapSeconds':overlap,'loopCrossfadeIntervals':[[i*(duration-overlap),i*(duration-overlap)+overlap] for i in range(1,copies)],'musicGainDb':gains,'sceneBoundariesSeconds':[s['startFrame']/c['fps'] for s in scenes]+[total],'originalAudioGainBeforeMaster':1,'masterGainDb':c['masterGainDb'],'limiterOrDialogueNormalizationApplied':False,'unencodedMixPeakDbFS':20*math.log10(peak),'musicStem':str(stem),'fullDecode':'passed','audio':'Unity original soundtrack plus independently rendered music stem, followed by a configurable shared headroom trim; combined AAC 256kbps/48kHz. No audio timing changes.'}
    joins=[]
    for interval in report['loopCrossfadeIntervals']:
        for t in interval:
            i=round(t*rate)*2
            joins.append({'seconds':t,'boundarySampleJump':max(abs(music_samples[i+k]-music_samples[i-2+k]) for k in [0,1]),'surrounding100msMaximumSampleJump':max(abs(music_samples[j]-music_samples[j-2]) for j in range(i-4800,i+4800))})
    report['verification']={'originalAudioHasNoTimeOffsetInUnencodedMix':True,'dialoguePlusMusicSumMaximumFloatError':sum_error,'loopJoinSampleChecks':joins,'musicFinalStereoSample':list(music_samples[-2:]),'decodedOutputPeakDbFS':20*math.log10(max(abs(x) for x in floats(out)))}
    out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest');main(p.parse_args().manifest)
