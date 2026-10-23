import http.server
import socketserver
import json
import urllib.parse
import os
import sys

# Kök dizini import yoluna ekle
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Modülleri içe aktar
import importlib.util

def load_tool(rel_path, mod_name):
    full_path = os.path.join(ROOT_DIR, rel_path)
    spec = importlib.util.spec_from_file_location(mod_name, full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

aero_calc = load_tool("aerospace-engineering/aerodynamics/airfoil_analyzer.py", "aero_calc")
beam_calc = load_tool("mechanical-civil/structural-mechanics/beam_stress_calculator.py", "beam_calc")
electrical_calc = load_tool("automation-electronics/circuit-design/electrical_calculator.py", "electrical_calc")
fluid_calc = load_tool("chemical-process/process-engineering/fluid_thermal_calculator.py", "fluid_calc")
bess_calc = load_tool("energy-engineering/storage-grid/bess_storage_calculator.py", "bess_calc")
cycle_calc = load_tool("mechanical-civil/thermodynamics/cycle_calculator.py", "cycle_calc")
robotics_calc = load_tool("automation-electronics/robotics/kinematics_calculator.py", "robotics_calc")
econ_calc = load_tool("industrial-engineering/engineering-economics/capital_budgeting.py", "econ_calc")
vib_calc = load_tool("mechanical-civil/acoustics-vibration/vibration_analyzer.py", "vib_calc")

PORT = 8080

HTML_PAGE = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Engineering Tools - Web Dashboard</title>
    <style>
        :root {
            --bg-dark: #0d1117;
            --bg-card: #161b22;
            --border: #30363d;
            --text-main: #f0f6fc;
            --text-muted: #8b949e;
            --primary: #58a6ff;
            --success: #3fb950;
            --warning: #d29922;
            --danger: #f85149;
            --purple: #bc8cff;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            display: flex;
            min-height: 100vh;
        }
        /* Sidebar */
        aside {
            width: 280px;
            background-color: var(--bg-card);
            border-right: 1px solid var(--border);
            padding: 24px 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .logo-area {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.15rem;
            font-weight: bold;
            color: var(--primary);
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        .nav-btn {
            background: none;
            border: 1px solid transparent;
            color: var(--text-muted);
            padding: 10px 14px;
            border-radius: 6px;
            text-align: left;
            font-size: 0.92rem;
            cursor: pointer;
            transition: all 0.2s ease;
            font-weight: 500;
        }
        .nav-btn:hover { background-color: rgba(88, 166, 255, 0.1); color: var(--text-main); }
        .nav-btn.active {
            background-color: #21262d;
            border-color: var(--border);
            color: var(--primary);
            font-weight: bold;
        }
        /* Main Content */
        main {
            flex: 1;
            padding: 32px;
            overflow-y: auto;
        }
        .header {
            margin-bottom: 24px;
        }
        .header h1 { font-size: 1.6rem; color: var(--text-main); margin-bottom: 6px; }
        .header p { color: var(--text-muted); font-size: 0.95rem; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        /* Cards */
        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .card h2 { font-size: 1.25rem; color: var(--primary); margin-bottom: 16px; }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 6px;
            font-weight: 500;
        }
        .form-group input, .form-group select {
            width: 100%;
            background-color: #0d1117;
            border: 1px solid var(--border);
            color: var(--text-main);
            padding: 9px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
            outline: none;
        }
        .form-group input:focus, .form-group select:focus {
            border-color: var(--primary);
        }
        button.calc-btn {
            background-color: #238636;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        button.calc-btn:hover { background-color: #2ea043; }
        /* Results */
        .results-area {
            margin-top: 24px;
            background-color: #0d1117;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 16px;
            display: none;
        }
        .results-area h3 { font-size: 1rem; color: var(--success); margin-bottom: 12px; }
        .res-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
        .res-table td { padding: 8px 12px; border-bottom: 1px solid #21262d; }
        .res-table td:first-child { color: var(--text-muted); width: 45%; }
        .res-table td:last-child { color: var(--text-main); font-weight: 600; }
        /* SVG Canvas */
        .chart-box {
            margin-top: 16px;
            background-color: #090d13;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 12px;
            text-align: center;
        }
        svg { width: 100%; height: 180px; }
    </style>
</head>
<body>
    <aside>
        <div class="logo-area">
            🛠️ Engineering Tools
        </div>
        <button class="nav-btn active" onclick="switchTab('beam')">🏗️ Kiriş & Mukavemet</button>
        <button class="nav-btn" onclick="switchTab('aero')">✈️ Havacılık & Atmosfer</button>
        <button class="nav-btn" onclick="switchTab('electric')">⚡ Kablo Gerilim Düşümü</button>
        <button class="nav-btn" onclick="switchTab('fluid')">🧪 Boru Basınç Kaybı</button>
        <button class="nav-btn" onclick="switchTab('bess')">🔋 Batarya BESS & LCOS</button>
        <button class="nav-btn" onclick="switchTab('econ')">💰 Sermaye Bütçeleme (NPV)</button>
        <button class="nav-btn" onclick="switchTab('vib')">🔊 Titreşim & Akustik</button>
    </aside>

    <main>
        <!-- 1. KİRİŞ VE MUKAVEMET -->
        <div id="tab-beam" class="tab-content active">
            <div class="header">
                <h1>Euler-Bernoulli Kiriş Eğilme ve Sehim Analizi</h1>
                <p>Kesit boyutları ve yükleme koşullarına göre eğilme gerilmesi, emniyet faktörü ve elastik çökme hesabı.</p>
            </div>
            <div class="card">
                <h2>Parametreler</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Genişlik b (mm)</label>
                        <input type="number" id="beam-b" value="50">
                    </div>
                    <div class="form-group">
                        <label>Yükseklik h (mm)</label>
                        <input type="number" id="beam-h" value="100">
                    </div>
                    <div class="form-group">
                        <label>Kiriş Açıklığı L (m)</label>
                        <input type="number" id="beam-l" value="3.0" step="0.1">
                    </div>
                    <div class="form-group">
                        <label>Ortadan Tekil Yük F (N)</label>
                        <input type="number" id="beam-f" value="4000">
                    </div>
                </div>
                <button class="calc-btn" onclick="calcBeam()">Kiriş Analizini Çalıştır</button>

                <div id="res-beam" class="results-area">
                    <h3>Sonuçlar</h3>
                    <table class="res-table" id="table-beam"></table>
                    <div class="chart-box">
                        <svg id="svg-beam" viewBox="0 0 500 150">
                            <!-- Dinamik Sehim Eğrisi -->
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. HAVACILIK VE ATMOSFER -->
        <div id="tab-aero" class="tab-content">
            <div class="header">
                <h1>Uluslararası Standart Atmosfer (ISA) ve Mach Modeli</h1>
                <p>İrtifaya bağlı sıcaklık, basınç, hava yoğunluğu, ses hızı ve dinamik basınç analizi.</p>
            </div>
            <div class="card">
                <h2>Uçuş Koşulları</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>İrtifa (metre, 0 - 20000)</label>
                        <input type="number" id="aero-alt" value="10000">
                    </div>
                    <div class="form-group">
                        <label>Uçuş Hızı (km/h)</label>
                        <input type="number" id="aero-v" value="850">
                    </div>
                </div>
                <button class="calc-btn" onclick="calcAero()">Atmosfer Analizini Çalıştır</button>

                <div id="res-aero" class="results-area">
                    <h3>Atmosferik Sonuçlar</h3>
                    <table class="res-table" id="table-aero"></table>
                </div>
            </div>
        </div>

        <!-- 3. ELEKTRİK KABLO GERİLİM DÜŞÜMÜ -->
        <div id="tab-electric" class="tab-content">
            <div class="header">
                <h1>Kablo Kesiti ve Gerilim Düşümü (IEC 60364)</h1>
                <p>Hat metrajı ve akımına bağlı voltaj düşümü ve standart sınır uygunluğu.</p>
            </div>
            <div class="card">
                <h2>Sistem Parametreleri</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Nominal Gerilim (V)</label>
                        <input type="number" id="el-v" value="400">
                    </div>
                    <div class="form-group">
                        <label>Hat Akımı (Amper)</label>
                        <input type="number" id="el-i" value="35">
                    </div>
                    <div class="form-group">
                        <label>Mesafe (metre)</label>
                        <input type="number" id="el-l" value="80">
                    </div>
                    <div class="form-group">
                        <label>Kablo Kesiti (mm²)</label>
                        <input type="number" id="el-s" value="10">
                    </div>
                </div>
                <button class="calc-btn" onclick="calcElectric()">Gerilim Düşümünü Hesapla</button>

                <div id="res-electric" class="results-area">
                    <h3>Sonuçlar</h3>
                    <table class="res-table" id="table-electric"></table>
                </div>
            </div>
        </div>

        <!-- 4. BORU BASINÇ KAYBI -->
        <div id="tab-fluid" class="tab-content">
            <div class="header">
                <h1>Darcy-Weisbach Boru Basınç Kaybı & Reynolds</h1>
                <p>Boru çapı ve debiye göre akış rejimi, sürtünme katsayısı ve basınç düşüşü.</p>
            </div>
            <div class="card">
                <h2>Hidrolik Parametreler</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Hacimsel Debi (m³/h)</label>
                        <input type="number" id="fluid-q" value="15">
                    </div>
                    <div class="form-group">
                        <label>Boru İç Çapı (mm)</label>
                        <input type="number" id="fluid-d" value="50">
                    </div>
                    <div class="form-group">
                        <label>Boru Boyu (m)</label>
                        <input type="number" id="fluid-l" value="60">
                    </div>
                </div>
                <button class="calc-btn" onclick="calcFluid()">Hidrolik Analizi Çalıştır</button>

                <div id="res-fluid" class="results-area">
                    <h3>Hidrolik Sonuçlar</h3>
                    <table class="res-table" id="table-fluid"></table>
                </div>
            </div>
        </div>

        <!-- 5. BESS BATARYA DEPOLAMA -->
        <div id="tab-bess" class="tab-content">
            <div class="header">
                <h1>BESS Batarya Depolama & LCOS Boyutlandırma</h1>
                <p>Günlük tüketim ve otonomi gününe göre akü kapasitesi (kWh, Ah) ve birim maliyet hesabı.</p>
            </div>
            <div class="card">
                <h2>Depolama Parametreleri</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Günlük Tüketim (kWh)</label>
                        <input type="number" id="bess-kwh" value="25">
                    </div>
                    <div class="form-group">
                        <label>Otonomi Süresi (Gün)</label>
                        <input type="number" id="bess-days" value="1.5" step="0.5">
                    </div>
                    <div class="form-group">
                        <label>Sistem Gerilimi (V)</label>
                        <input type="number" id="bess-v" value="48">
                    </div>
                </div>
                <button class="calc-btn" onclick="calcBess()">BESS Boyutlandırmasını Yap</button>

                <div id="res-bess" class="results-area">
                    <h3>Depolama Sonuçları</h3>
                    <table class="res-table" id="table-bess"></table>
                </div>
            </div>
        </div>

        <!-- 6. SERMAYE BÜTÇELEME (NPV) -->
        <div id="tab-econ" class="tab-content">
            <div class="header">
                <h1>Mühendislik Ekonomisi: NPV & IRR Analizi</h1>
                <p>Yatırım sermaye bütçelemesi, iç karlılık oranı ve geri ödeme süresi.</p>
            </div>
            <div class="card">
                <h2>Fizibilite Girdileri</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>İlk Yatırım ($ C0)</label>
                        <input type="number" id="econ-c0" value="80000">
                    </div>
                    <div class="form-group">
                        <label>İskonto Oranı (% r)</label>
                        <input type="number" id="econ-r" value="10">
                    </div>
                    <div class="form-group" style="grid-column: span 2;">
                        <label>Yıllık Nakit Girişleri ($ boşlukla ayırın)</label>
                        <input type="text" id="econ-cfs" value="25000 28000 32000 35000 40000">
                    </div>
                </div>
                <button class="calc-btn" onclick="calcEcon()">Fizibilite Analizini Çalıştır</button>

                <div id="res-econ" class="results-area">
                    <h3>Finansal Değerlendirme</h3>
                    <table class="res-table" id="table-econ"></table>
                </div>
            </div>
        </div>

        <!-- 7. TİTREŞİM VE AKUSTİK -->
        <div id="tab-vib" class="tab-content">
            <div class="header">
                <h1>Mekanik Titreşim (SDOF) ve Akustik Analiz</h1>
                <p>Doğal frekans, sönüm rejimi ve rezonans risk denetimi.</p>
            </div>
            <div class="card">
                <h2>Sistem Parametreleri</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Kütle m (kg)</label>
                        <input type="number" id="vib-m" value="60">
                    </div>
                    <div class="form-group">
                        <label>Yay Sertliği k (N/m)</label>
                        <input type="number" id="vib-k" value="25000">
                    </div>
                    <div class="form-group">
                        <label>Sönüm Katsayısı c (N·s/m)</label>
                        <input type="number" id="vib-c" value="90">
                    </div>
                    <div class="form-group">
                        <label>Tahrik Frekansı (Hz)</label>
                        <input type="number" id="vib-f" value="3.5" step="0.1">
                    </div>
                </div>
                <button class="calc-btn" onclick="calcVib()">Titreşim Analizini Çalıştır</button>

                <div id="res-vib" class="results-area">
                    <h3>Dinamik Analiz Sonuçları</h3>
                    <table class="res-table" id="table-vib"></table>
                </div>
            </div>
        </div>
    </main>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            event.target.classList.add('active');
        }

        async function postAPI(endpoint, data) {
            const resp = await fetch('/api/' + endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            return await resp.json();
        }

        function renderTable(tableId, data) {
            const tbody = document.getElementById(tableId);
            tbody.innerHTML = '';
            for (const [k, v] of Object.entries(data)) {
                const tr = document.createElement('tr');
                const tdKey = document.createElement('td');
                const tdVal = document.createElement('td');
                tdKey.textContent = k;
                tdVal.textContent = typeof v === 'number' ? v.toFixed(3) : v;
                tr.appendChild(tdKey);
                tr.appendChild(tdVal);
                tbody.appendChild(tr);
            }
        }

        async function calcBeam() {
            const b = parseFloat(document.getElementById('beam-b').value);
            const h = parseFloat(document.getElementById('beam-h').value);
            const l = parseFloat(document.getElementById('beam-l').value);
            const f = parseFloat(document.getElementById('beam-f').value);
            const data = await postAPI('beam', { b, h, l, f });
            
            renderTable('table-beam', data);
            document.getElementById('res-beam').style.display = 'block';

            // SVG Sehim Eğrisi Çiz
            const svg = document.getElementById('svg-beam');
            svg.innerHTML = `
                <line x1="40" y1="50" x2="460" y2="50" stroke="#8b949e" stroke-dasharray="4" stroke-width="1.5" />
                <path d="M 40 50 Q 250 120 460 50" fill="none" stroke="#58a6ff" stroke-width="3" />
                <polygon points="40,50 30,70 50,70" fill="#3fb950" />
                <polygon points="460,50 450,70 470,70" fill="#3fb950" />
                <line x1="250" y1="10" x2="250" y2="45" stroke="#f85149" stroke-width="3" />
                <polygon points="250,50 245,35 255,35" fill="#f85149" />
                <text x="255" y="30" fill="#f85149" font-size="12" font-weight="bold">F = ${f} N</text>
                <text x="250" y="140" fill="#58a6ff" font-size="12" text-anchor="middle">Maksimum Sehim</text>
            `;
        }

        async function calcAero() {
            const alt = parseFloat(document.getElementById('aero-alt').value);
            const v = parseFloat(document.getElementById('aero-v').value);
            const data = await postAPI('aero', { alt, v });
            renderTable('table-aero', data);
            document.getElementById('res-aero').style.display = 'block';
        }

        async function calcElectric() {
            const v = parseFloat(document.getElementById('el-v').value);
            const i = parseFloat(document.getElementById('el-i').value);
            const l = parseFloat(document.getElementById('el-l').value);
            const s = parseFloat(document.getElementById('el-s').value);
            const data = await postAPI('electric', { v, i, l, s });
            renderTable('table-electric', data);
            document.getElementById('res-electric').style.display = 'block';
        }

        async function calcFluid() {
            const q = parseFloat(document.getElementById('fluid-q').value);
            const d = parseFloat(document.getElementById('fluid-d').value);
            const l = parseFloat(document.getElementById('fluid-l').value);
            const data = await postAPI('fluid', { q, d, l });
            renderTable('table-fluid', data);
            document.getElementById('res-fluid').style.display = 'block';
        }

        async function calcBess() {
            const kwh = parseFloat(document.getElementById('bess-kwh').value);
            const days = parseFloat(document.getElementById('bess-days').value);
            const v = parseFloat(document.getElementById('bess-v').value);
            const data = await postAPI('bess', { kwh, days, v });
            renderTable('table-bess', data);
            document.getElementById('res-bess').style.display = 'block';
        }

        async function calcEcon() {
            const c0 = parseFloat(document.getElementById('econ-c0').value);
            const r = parseFloat(document.getElementById('econ-r').value) / 100.0;
            const cfs = document.getElementById('econ-cfs').value.split(' ').map(x => parseFloat(x));
            const data = await postAPI('econ', { c0, r, cfs });
            renderTable('table-econ', data);
            document.getElementById('res-econ').style.display = 'block';
        }

        async function calcVib() {
            const m = parseFloat(document.getElementById('vib-m').value);
            const k = parseFloat(document.getElementById('vib-k').value);
            const c = parseFloat(document.getElementById('vib-c').value);
            const f = parseFloat(document.getElementById('vib-f').value);
            const data = await postAPI('vib', { m, k, c, f });
            renderTable('table-vib', data);
            document.getElementById('res-vib').style.display = 'block';
        }
    </script>
</body>
</html>
"""

class EngineeringServerHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path.startswith("/assets/"):
            file_path = os.path.join(ROOT_DIR, self.path.lstrip("/"))
            if os.path.exists(file_path):
                self.send_response(200)
                if file_path.endswith(".png"):
                    self.send_header("Content-Type", "image/png")
                elif file_path.endswith(".jpg"):
                    self.send_header("Content-Type", "image/jpeg")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        req_json = json.loads(post_data.decode('utf-8'))
        
        response_data = {}
        
        if self.path == "/api/beam":
            b = req_json.get("b", 50)
            h = req_json.get("h", 100)
            l = req_json.get("l", 3.0)
            f = req_json.get("f", 4000)
            sec, _ = beam_calc.calculate_section_properties("rectangle", b=b, h=h)
            res, _ = beam_calc.calculate_beam_mechanics(1, f, l, sec["Atalet Momenti Ix (mm⁴)"], sec["Mukavemet Momenti Wx (mm³)"], 210.0, 235.0)
            response_data = res

        elif self.path == "/api/aero":
            alt = req_json.get("alt", 0)
            v = req_json.get("v", 0)
            res, _ = aero_calc.calculate_isa_atmosphere(alt, v)
            response_data = res

        elif self.path == "/api/electric":
            v = req_json.get("v", 400)
            i = req_json.get("i", 30)
            l = req_json.get("l", 50)
            s = req_json.get("s", 10)
            res, _ = electrical_calc.calculate_voltage_drop(v, i, l, s, material="bakir", system_type="3phase")
            response_data = res

        elif self.path == "/api/fluid":
            q = req_json.get("q", 10)
            d = req_json.get("d", 50)
            l = req_json.get("l", 50)
            res, _ = fluid_calc.calculate_pipe_friction(q, d, l)
            response_data = res

        elif self.path == "/api/bess":
            kwh = req_json.get("kwh", 20)
            days = req_json.get("days", 1.0)
            v = req_json.get("v", 48)
            res, _ = bess_calc.calculate_bess_sizing(kwh, days, v)
            response_data = res

        elif self.path == "/api/econ":
            c0 = req_json.get("c0", 100000)
            r = req_json.get("r", 0.10)
            cfs = req_json.get("cfs", [25000, 30000, 35000])
            res, _ = econ_calc.analyze_capital_budgeting(c0, cfs, r)
            response_data = res

        elif self.path == "/api/vib":
            m = req_json.get("m", 50)
            k = req_json.get("k", 20000)
            c = req_json.get("c", 50)
            f = req_json.get("f", 3.0)
            res, _ = vib_calc.calculate_sdof_vibration(m, k, c, f)
            response_data = res

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        # Konsolu sessiz tut
        pass

def start_server(port=PORT):
    server_address = ('', port)
    with socketserver.TCPServer(server_address, EngineeringServerHandler) as httpd:
        print(f"\n🚀 [Engineering Tools] Web Dashboard Aktif: http://localhost:{port}")
        print("Durdurmak için Ctrl+C tuşlarına basın...\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nWeb sunucusu durduruldu.")

if __name__ == "__main__":
    start_server()
