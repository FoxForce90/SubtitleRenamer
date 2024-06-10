import os
import tkinter as tk
from tkinter import filedialog, messagebox

# List of video file extensions (add more if needed)
video_extensions = ['.mp4', '.mkv', '.avi', '.mov']

# List of subtitle file extensions (add more if needed)
subtitle_extensions = ['.srt', '.sub', '.ass']

def get_files_with_extensions(directory, extensions):
    return [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in extensions]

def rename_subtitles_to_match_videos(video_directory, subtitle_directory):
    video_files = get_files_with_extensions(video_directory, video_extensions)
    subtitle_files = get_files_with_extensions(subtitle_directory, subtitle_extensions)
    
    video_files.sort()
    subtitle_files.sort()

    if len(video_files) != len(subtitle_files):
        messagebox.showwarning("Warning", "The number of video files and subtitle files does not match.")
        return

    for video_file, subtitle_file in zip(video_files, subtitle_files):
        video_name, video_ext = os.path.splitext(video_file)
        subtitle_name, subtitle_ext = os.path.splitext(subtitle_file)
        
        new_subtitle_name = f"{video_name}{subtitle_ext}"
        
        old_subtitle_path = os.path.join(subtitle_directory, subtitle_file)
        new_subtitle_path = os.path.join(subtitle_directory, new_subtitle_name)
        
        os.rename(old_subtitle_path, new_subtitle_path)
    
    messagebox.showinfo("Success", "Subtitles have been renamed to match the videos.")
    update_file_lists(video_directory, subtitle_directory)

def browse_directory(entry_field, file_list, extensions):
    directory = filedialog.askdirectory()
    if directory:
        entry_field.delete(0, tk.END)
        entry_field.insert(0, directory)
        update_file_list(file_list, directory, extensions)

def update_file_list(file_list, directory, extensions):
    file_list.delete(0, tk.END)
    if directory:
        files = get_files_with_extensions(directory, extensions)
        for file in files:
            file_list.insert(tk.END, file)

def start_renaming():
    video_directory = entry_video_directory.get()
    subtitle_directory = entry_subtitle_directory.get()

    if os.path.isdir(video_directory) and os.path.isdir(subtitle_directory):
        rename_subtitles_to_match_videos(video_directory, subtitle_directory)
    else:
        messagebox.showerror("Error", "Invalid directories. Please select valid directories for both videos and subtitles.")

# Create the main window
root = tk.Tk()
root.title("Subtitle Renamer")

# Video directory selection
frame_video_directory = tk.Frame(root)
frame_video_directory.pack(padx=10, pady=5)

label_video_directory = tk.Label(frame_video_directory, text="Select Video Directory:")
label_video_directory.pack(side=tk.LEFT)

entry_video_directory = tk.Entry(frame_video_directory, width=50)
entry_video_directory.pack(side=tk.LEFT, padx=5)

button_browse_video = tk.Button(frame_video_directory, text="Browse", command=lambda: browse_directory(entry_video_directory, video_list, video_extensions))
button_browse_video.pack(side=tk.LEFT)

# Subtitle directory selection
frame_subtitle_directory = tk.Frame(root)
frame_subtitle_directory.pack(padx=10, pady=5)

label_subtitle_directory = tk.Label(frame_subtitle_directory, text="Select Subtitle Directory:")
label_subtitle_directory.pack(side=tk.LEFT)

entry_subtitle_directory = tk.Entry(frame_subtitle_directory, width=50)
entry_subtitle_directory.pack(side=tk.LEFT, padx=5)

button_browse_subtitle = tk.Button(frame_subtitle_directory, text="Browse", command=lambda: browse_directory(entry_subtitle_directory, subtitle_list, subtitle_extensions))
button_browse_subtitle.pack(side=tk.LEFT)

# File lists
frame_file_lists = tk.Frame(root)
frame_file_lists.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

label_videos = tk.Label(frame_file_lists, text="Video Files:")
label_videos.pack(side=tk.LEFT, padx=10)

video_list = tk.Listbox(frame_file_lists, width=50, height=20)
video_list.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

label_subtitles = tk.Label(frame_file_lists, text="Subtitle Files:")
label_subtitles.pack(side=tk.LEFT, padx=10)

subtitle_list = tk.Listbox(frame_file_lists, width=50, height=20)
subtitle_list.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

# Rename button
button_rename = tk.Button(root, text="Rename Subtitles", command=start_renaming)
button_rename.pack(pady=10)

# Start the GUI event loop
root.mainloop()
