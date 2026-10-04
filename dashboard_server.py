# encoding: utf-8
"""Viral Meme Curator - Modern Web Dashboard Server (Flask)."""

import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from flask import Flask, jsonify, render_template_string, request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Viral Meme Curator - 自动化发布统计 Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', system-ui, -apple-system, sans-serif; }
    .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .glow-card { transition: all 0.3s ease; }
    .glow-card:hover { transform: translateY(-3px); box-shadow: 0 10px 30px -10px rgba(59, 130, 246, 0.4); }
  </style>
</head>
<body class="min-h-screen pb-12">
  <!-- Top Nav -->
  <nav class="glass sticky top-0 z-50 px-8 py-4 flex items-center justify-between border-b border-slate-800">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-bold text-xl shadow-lg shadow-blue-500/30">
        🔥
      </div>
      <div>
        <h1 class="font-bold text-lg leading-none bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">Viral Meme Curator</h1>
        <p class="text-xs text-slate-400 mt-1">U.S. Gen-Z 爆梗全自动发布统计面板</p>
      </div>
    </div>
    <div class="flex items-center gap-4">
      <button onclick="triggerPipeline()" id="btn-trigger" class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium text-sm transition shadow-lg shadow-blue-500/25 flex items-center gap-2">
        <i class="fa-solid fa-bolt"></i> 立即一键抓取并发布
      </button>
      <button onclick="refreshData()" class="p-2.5 rounded-xl glass hover:bg-slate-800 text-slate-300 transition">
        <i class="fa-solid fa-rotate-right"></i>
      </button>
    </div>
  </nav>

  <main class="max-w-7xl mx-auto px-8 mt-8 space-y-8">
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="glass p-6 rounded-2xl glow-card">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">累计已发送推文</span>
          <span class="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center"><i class="fa-brands fa-x-twitter"></i></span>
        </div>
        <div class="text-3xl font-extrabold mt-3 text-white" id="stat-total">0</div>
        <div class="text-xs text-slate-400 mt-2 flex items-center gap-1">
          <span class="text-emerald-400 font-medium">100%</span> 成功投递
        </div>
      </div>

      <div class="glass p-6 rounded-2xl glow-card">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">成功发布计数</span>
          <span class="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center"><i class="fa-solid fa-circle-check"></i></span>
        </div>
        <div class="text-3xl font-extrabold mt-3 text-emerald-400" id="stat-success">0</div>
        <div class="text-xs text-slate-400 mt-2">实时状态监测</div>
      </div>

      <div class="glass p-6 rounded-2xl glow-card">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">异常与拦截</span>
          <span class="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center"><i class="fa-solid fa-triangle-exclamation"></i></span>
        </div>
        <div class="text-3xl font-extrabold mt-3 text-slate-200" id="stat-error">0</div>
        <div class="text-xs text-slate-400 mt-2">自动风控熔断保护</div>
      </div>

      <div class="glass p-6 rounded-2xl glow-card">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">防封保护引擎</span>
          <span class="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center"><i class="fa-solid fa-shield-halved"></i></span>
        </div>
        <div class="text-lg font-bold mt-3 text-indigo-300">Patchright Stealth</div>
        <div class="text-xs text-emerald-400 mt-2">● 隐身伪装已生效</div>
      </div>
    </div>

    <!-- History Table -->
    <div class="glass rounded-2xl p-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-lg font-bold text-white">推文发送历史明细</h2>
          <p class="text-xs text-slate-400 mt-1">展示最新自动抓取、美化重构与发推记录</p>
        </div>
        <span id="last-update" class="text-xs text-slate-500">更新于: -</span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse text-sm">
          <thead>
            <tr class="border-b border-slate-800 text-slate-400 text-xs uppercase">
              <th class="py-3 px-4">发送时间</th>
              <th class="py-3 px-4">发布平台</th>
              <th class="py-3 px-4">美式 Gen-Z 重构推文内容</th>
              <th class="py-3 px-4">状态</th>
            </tr>
          </thead>
          <tbody id="history-tbody" class="divide-y divide-slate-800 text-slate-300">
            <tr>
              <td colspan="4" class="py-8 text-center text-slate-500">暂无发送历史数据，请点击右上方“立即一键抓取并发布”</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <script>
    async function refreshData() {
      try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        
        document.getElementById('stat-total').innerText = data.total || 0;
        document.getElementById('stat-success').innerText = data.success || 0;
        document.getElementById('stat-error').innerText = data.error || 0;
        document.getElementById('last-update').innerText = '最后更新: ' + new Date().toLocaleTimeString();

        const historyRes = await fetch('/api/history');
        const historyData = await historyRes.json();
        renderHistory(historyData);
      } catch (e) {
        console.error('Error refreshing stats:', e);
      }
    }

    function renderHistory(items) {
      const tbody = document.getElementById('history-tbody');
      if (!items || items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="py-8 text-center text-slate-500">暂无发送历史数据，请点击右上方“立即一键抓取并发布”</td></tr>`;
        return;
      }
      
      tbody.innerHTML = items.reverse().map(item => `
        <tr class="hover:bg-slate-800/40 transition">
          <td class="py-4 px-4 text-xs whitespace-nowrap text-slate-400">${item.timestamp || '-'}</td>
          <td class="py-4 px-4 text-xs font-semibold text-blue-400 uppercase">${item.platform || 'Twitter/X'}</td>
          <td class="py-4 px-4 text-sm font-mono whitespace-pre-wrap max-w-xl text-slate-200">${escapeHtml(item.content || '')}</td>
          <td class="py-4 px-4 whitespace-nowrap">
            ${item.status === 'success' 
              ? '<span class="px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">✅ 发送成功</span>'
              : `<span class="px-2.5 py-1 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">❌ 异常: ${escapeHtml(item.status)}</span>`}
          </td>
        </tr>
      `).join('');
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    async function triggerPipeline() {
      const btn = document.getElementById('btn-trigger');
      btn.disabled = true;
      btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> 正在抓取、重构并发布中...`;
      
      try {
        const res = await fetch('/api/trigger', { method: 'POST' });
        const data = await res.json();
        alert(data.msg || '抓取与发布流程已拉起！后台发布完成后会自动刷新明细。');
      } catch (e) {
        alert('触发失败: ' + e);
      } finally {
        setTimeout(() => {
          btn.disabled = false;
          btn.innerHTML = `<i class="fa-solid fa-bolt"></i> 立即一键抓取并发布`;
          refreshData();
        }, 5000);
      }
    }

    refreshData();
    setInterval(refreshData, 10000);
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    history_path = BASE_DIR / "temp" / "history.json"
    if not history_path.exists():
        return jsonify({"total": 0, "success": 0, "error": 0})
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            items = json.load(f)
        total = len(items)
        success = sum(1 for i in items if i.get("status") == "success")
        error = total - success
        return jsonify({"total": total, "success": success, "error": error})
    except Exception as e:
        return jsonify({"total": 0, "success": 0, "error": 0, "msg": str(e)})

@app.route('/api/history', methods=['GET'])
def get_history():
    history_path = BASE_DIR / "temp" / "history.json"
    if not history_path.exists():
        return jsonify([])
    try:
        with open(history_path, "r", encoding="utf-8") as f:
            items = json.load(f)
        return jsonify(items)
    except Exception:
        return jsonify([])

def run_pipeline_task():
    try:
        subprocess.run([sys.executable, "scripts/fetch_reddit_trending.py", "--subreddit", "memes", "--limit", "3"], cwd=BASE_DIR, check=True)
        subprocess.run([sys.executable, "scripts/meme_rewriter.py", "--input-file", "temp/reddit_trending.json"], cwd=BASE_DIR, check=True)
        subprocess.run([sys.executable, "scripts/auto_publisher.py"], cwd=BASE_DIR, check=True)
    except Exception as e:
        print(f"Pipeline execution error: {e}")

@app.route('/api/trigger', methods=['POST'])
def trigger_pipeline():
    thread = threading.Thread(target=run_pipeline_task)
    thread.start()
    return jsonify({"code": 200, "msg": "一键抓取、改写与发布管线已成功拉起，发布完成后面板会自动实时更新统计！"})

if __name__ == '__main__':
    print("🚀 Viral Meme Curator Dashboard is running on http://localhost:5050")
    app.run(host='0.0.0.0', port=5050, debug=False)
