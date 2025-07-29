import whisperx

def transcribe_mp3_to_text(mp3_path, model_name="medium", language="zh"):
    model = whisperx.load_model(model_name, device="cuda", compute_type="float32")
    result = model.transcribe(mp3_path, language=language)
    return result["segments"]

if __name__ == "__main__":
    mp3_path = "20250717-1.m4a"  # 換成你要測試的 mp3 路徑
    text = transcribe_mp3_to_text(mp3_path)
    print(text)