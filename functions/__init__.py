import json
import re
import yt_dlp as YouTube
ydl_opts = {
    "quiet": True,
}

class Youtube_Extract:
    def __init__(self, link):
        ydl = YouTube.YoutubeDL(ydl_opts)
        self.info_dict = ydl.extract_info(link, download=False)
        self.video_title = self.info_dict.get("title", "")

    def get_info(self):
        video_id = self.info_dict.get("id", "")
        video_author = self.info_dict.get('channel', "")
        video_views = int(self.info_dict.get("view_count", ""))
        video_length = int(self.info_dict.get('duration', ''))
        print(video_length)
        video_thumnail = self.info_dict.get("thumbnail", "")

        return {
            "Id": video_id,
            "Title": self.video_title,
            "Channel": video_author,
            "Length": self.convert_seconds(video_length),
            "Views": self.convert_views(video_views),
            "Thumbnail": video_thumnail
        }

    def get_audio(self):
        data={}
        for i in self.info_dict["formats"]:
            if "audio_channels" in i and i["audio_channels"] == 2 and i["resolution"] == "audio only":
                ext=i['ext']
                Format=i['format'].replace(' audio only ', ' ')
                url=i['url']+f"&dl=1&title={self.title_to_slug(self.video_title)}"
                data[Format]=url

        return data

    def get_video(self):
        data={}
        for i in self.info_dict["formats"]:
            if "audio_channels" in i and i["audio_channels"] == 2 and i["resolution"] not in ["audio only", "144p"]:
                q = ["360p", "720p"]
                if i["format_note"] in q:
                    Format=i['format_note']
                    url=i.get('url', 'N/A')+f"&dl=1&title={self.title_to_slug(self.video_title)}"
                    data[Format]=url
                    # ext=i.get('video_ext', 'N/A')
        return data

    def convert_seconds(self,time_in_seconds):
        if time_in_seconds < 60:
            return f"00:{time_in_seconds:02}"
        elif time_in_seconds < 3600:
            minutes = time_in_seconds // 60
            seconds = time_in_seconds % 60
            return f"{minutes:02}:{seconds:02}"
        else:
            hours = time_in_seconds // 3600
            minutes = (time_in_seconds % 3600) // 60
            seconds = time_in_seconds % 60
            return f"{hours:02}:{minutes:02}:{seconds:02}"

    def convert_views(self,views):
        if views < 1000:
            return f"{views}"
        elif views < 1_000_000:
            return f"{views / 1000:.1f}K"
        elif views < 1_000_000_000:
            return f"{views / 1_000_000:.1f}M"
        else:
            return f"{views / 1_000_000_000:.1f}B"
    def title_to_slug(self,title):
        slug= re.sub(r'[^a-zA-Z0-9]+', '-', re.sub(r'[^\w\s-]', '', title).strip().lower())
        return slug
