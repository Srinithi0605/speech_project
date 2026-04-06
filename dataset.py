# dataset.py

data = [

# 🎵 MUSIC
("play music", "music"),
("play some music", "music"),
("start music", "music"),
("play songs", "music"),
("play a song", "music"),
("can you play music", "music"),
("please play music", "music"),
("i want to listen to music", "music"),
("play something", "music"),
("play any music", "music"),
("play tamil songs", "music"),
("play english songs", "music"),
("play melody songs", "music"),
("play latest songs", "music"),
("play old songs", "music"),
("play random music", "music"),
("start playing songs", "music"),
("put on some music", "music"),
("play musc", "music"),
("play musics", "music"),

# 🔇 MUTE
("mute", "mute"),
("mute audio", "mute"),
("mute sound", "mute"),
("turn off sound", "mute"),
("turn off audio", "mute"),
("silence audio", "mute"),
("disable sound", "mute"),
("mute the system", "mute"),
("stop sound", "mute"),
("no sound", "mute"),
("please mute", "mute"),
("can you mute", "mute"),

# 🔊 VOLUME UP
("volume up", "volume_up"),
("increase volume", "volume_up"),
("raise volume", "volume_up"),
("make volume higher", "volume_up"),
("turn volume up", "volume_up"),
("boost volume", "volume_up"),
("increase sound", "volume_up"),
("make it louder", "volume_up"),
("louder please", "volume_up"),
("volume increase", "volume_up"),
("can you increase volume", "volume_up"),

# 🔉 VOLUME DOWN
("volume down", "volume_down"),
("decrease volume", "volume_down"),
("lower volume", "volume_down"),
("turn volume down", "volume_down"),
("reduce volume", "volume_down"),
("make it quieter", "volume_down"),
("lower the sound", "volume_down"),
("soften the volume", "volume_down"),
("volume decrease", "volume_down"),
("can you lower volume", "volume_down"),

# 🌐 GOOGLE SEARCH
("search google", "google_search"),
("google search", "google_search"),
("search something", "google_search"),
("find something", "google_search"),
("look up something", "google_search"),
("search for news", "google_search"),
("search online", "google_search"),
("google it", "google_search"),
("can you search google", "google_search"),
("search the internet", "google_search"),
("look up python", "google_search"),
("find information", "google_search"),

# ▶ YOUTUBE
("open youtube", "youtube_search"),
("youtube", "youtube_search"),
("play youtube", "youtube_search"),
("search youtube", "youtube_search"),
("youtube videos", "youtube_search"),
("watch youtube", "youtube_search"),
("open you tube", "youtube_search"),
("launch youtube", "youtube_search"),
("go to youtube", "youtube_search"),
("play video on youtube", "youtube_search"),
("search videos", "youtube_search"),
("watch videos", "youtube_search"),

# 🖥️ OPEN APPS
("open chrome", "open_app"),
("launch chrome", "open_app"),
("start chrome", "open_app"),
("run chrome", "open_app"),
("open google chrome", "open_app"),
("can you open chrome", "open_app"),
("please open chrome", "open_app"),
("i want to open chrome", "open_app"),
("open chrome browser", "open_app"),
("chrome open", "open_app"),
("open chrom", "open_app"),
("start browser", "open_app"),

("open vscode", "open_app"),
("open visual studio code", "open_app"),
("launch vscode", "open_app"),
("start vscode", "open_app"),
("open code", "open_app"),
("vscode open", "open_app"),

("open spotify", "open_app"),
("start spotify", "open_app"),
("launch spotify", "open_app"),

("open calculator", "open_app"),
("start calculator", "open_app"),
("launch calculator", "open_app"),

("open notepad", "open_app"),
("start notepad", "open_app"),
("launch notepad", "open_app"),

# 📂 FILES
("open downloads", "files"),
("open documents", "files"),
("open desktop", "files"),
("show downloads", "files"),
("open my files", "files"),
("open folder", "files"),
("show documents", "files"),
("open my documents", "files"),
("go to downloads", "files"),
("open file manager", "files"),
("show my files", "files"),

# 📸 SCREENSHOT
("take screenshot", "screenshot"),
("capture screen", "screenshot"),
("screen shot", "screenshot"),
("take a screenshot", "screenshot"),
("capture my screen", "screenshot"),
("save screenshot", "screenshot"),
("take screen capture", "screenshot"),
("screenshot now", "screenshot"),
("click screenshot", "screenshot"),

# 🕒 TIME
("what time is it", "time"),
("tell me the time", "time"),
("current time", "time"),
("time now", "time"),
("show time", "time"),
("give me the time", "time"),
("what is current time", "time"),
("tell time now", "time"),
("can you tell time", "time"),

# ❌ EXIT
("exit", "exit"),
("quit", "exit"),
("close program", "exit"),
("stop program", "exit"),
("exit system", "exit"),
("terminate program", "exit"),
("close application", "exit"),
("stop everything", "exit"),
("shutdown assistant", "exit"),
("end program", "exit"),

# 🔥 ADDITIONS (FIXED - NO CONFLICTS)

# ✅ ONLY CLEAR explorer commands (no ambiguity)
("open file explorer", "open_app"),
("open explorer", "open_app"),
("launch file explorer", "open_app"),
("start explorer", "open_app"),
("open windows explorer", "open_app"),

# ✅ System apps
("open settings", "open_app"),
("open control panel", "open_app"),
("open task manager", "open_app"),

# ✅ Missing apps
("open whatsapp", "open_app"),
("launch whatsapp", "open_app"),
("start whatsapp", "open_app"),

("open photos", "open_app"),
("open camera", "open_app"),

# ✅ Folder clarity (safe)
("open downloads folder", "files"),
("open documents folder", "files"),
("open desktop folder", "files"),

]


# 🔥 AUTO DATASET EXPANSION

def expand_dataset(data):
    expanded = []

    for text, label in data:
        expanded.append((text, label))
        expanded.append((f"please {text}", label))
        expanded.append((f"can you {text}", label))
        expanded.append((f"{text} please", label))

    return expanded


texts = [x[0] for x in data]
labels = [x[1] for x in data]