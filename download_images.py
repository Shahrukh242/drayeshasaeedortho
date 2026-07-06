import os
import urllib.request

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(PROJECT_ROOT, 'assets', 'images', 'blog')
os.makedirs(BLOG_DIR, exist_ok=True)

IMAGES = {
    "clubfoot-care.jpg": "https://images.unsplash.com/photo-1584824486509-112e4181ff6b?auto=format&fit=crop&w=600&q=80",
    "bow-legs-children.jpg": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=600&q=80",
    "flat-feet-shoes.jpg": "https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&w=600&q=80",
    "scoliosis-screening.jpg": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=600&q=80",
    "rickets-prevention.jpg": "https://images.unsplash.com/photo-1595079676339-1534801ad6cf?auto=format&fit=crop&w=600&q=80",
    "growth-plate-fractures.jpg": "https://images.unsplash.com/photo-1486218119243-13883505764c?auto=format&fit=crop&w=600&q=80",
    "correct-sitting-posture.jpg": "https://images.unsplash.com/photo-1516627145497-ae6968895b74?auto=format&fit=crop&w=600&q=80",
    "stretching-for-kids.jpg": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=600&q=80",
    "screen-time-bone-health.jpg": "https://images.unsplash.com/photo-1463947628408-f8581a2f4aca?auto=format&fit=crop&w=600&q=80",
    "walking-delays-toddlers.jpg": "https://images.unsplash.com/photo-1510154221590-ff63e90a136f?auto=format&fit=crop&w=600&q=80",
    "hip-instability-infants.jpg": "https://images.unsplash.com/photo-1536640712-4d4c36ff0e4e?auto=format&fit=crop&w=600&q=80",
    "fractures-in-children.jpg": "https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?auto=format&fit=crop&w=600&q=80",
    "sports-injuries-young-athletes.jpg": "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=600&q=80",
    "bone-pain-in-children.jpg": "https://images.unsplash.com/photo-1519689680058-324335c77eba?auto=format&fit=crop&w=600&q=80"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for filename, url in IMAGES.items():
    filepath = os.path.join(BLOG_DIR, filename)
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Saved to {filepath}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
