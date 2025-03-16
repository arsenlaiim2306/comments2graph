# Comments2Graph 🔍→📊

**Tool for Visualizing Comments into Interactive 2D/3D Graphs**  
Analyze patterns, cluster, and explore YouTube comments through an ML-powered pipeline.

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/arsenlaiim2306/comments2graph.git
pip install -r requirements.txt
```

### Basic Usage
```bash
# For a YouTube video (auto-download via yt-dlp)
python -m comments2graph "https://youtube.com/watch?v=..."

# From a file with URLs (one per line)
python -m comments2graph links.txt
```

## ⚙️ Configuration
Create `config.json`:
```json
{
  "youtube_api": {
    "developerKey": "YOUR_API_KEY"
  },
  "dbscan": {
    "eps": 0.4,
    "min_samples": 3
  },
  "umap": {
    "n_components": 3  # 2 for 2D, 3 for 3D
  }
}
```