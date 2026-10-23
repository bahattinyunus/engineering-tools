import unittest
import importlib.util
import os
import sys
import math

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def import_from_path(rel_path, module_name=None):
    full_path = os.path.join(ROOT_DIR, rel_path)
    if module_name is None:
        module_name = os.path.splitext(os.path.basename(rel_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Mevcut modülleri yükle
data_analyzer = import_from_path("software/python/data_analyzer.py")
cloud_cost = import_from_path("software/cloud/cloud_cost_calculator.py")
algo_bench = import_from_path("software/algorithms/complexity_benchmarker.py")
electrical_calc = import_from_path("automation-electronics/circuit-design/electrical_calculator.py")
modbus_sim = import_from_path("automation-electronics/plc-scada/modbus_simulator.py")
robotics_calc = import_from_path("automation-electronics/robotics/kinematics_calculator.py")
gcode_gen = import_from_path("mechanical-civil/cad-cam/gcode_generator.py")
cpm_calc = import_from_path("mechanical-civil/project-management/cpm_calculator.py")
beam_calc = import_from_path("mechanical-civil/structural-mechanics/beam_stress_calculator.py")
cycle_calc = import_from_path("mechanical-civil/thermodynamics/cycle_calculator.py")
fluid_calc = import_from_path("chemical-process/process-engineering/fluid_thermal_calculator.py")
oee_calc = import_from_path("industrial-engineering/lean-six-sigma/oee_sigma_calculator.py")
carbon_calc = import_from_path("environment/sustainability-reports/carbon_footprint.py")
power_calc = import_from_path("energy-engineering/renewables/power_calculator.py")
bess_calc = import_from_path("energy-engineering/storage-grid/bess_storage_calculator.py")
aero_calc = import_from_path("aerospace-engineering/aerodynamics/airfoil_analyzer.py")
vib_calc = import_from_path("mechanical-civil/acoustics-vibration/vibration_analyzer.py")
econ_calc = import_from_path("industrial-engineering/engineering-economics/capital_budgeting.py")


class TestSoftwareTools(unittest.TestCase):
    def test_stats_calculation(self):
        data = [10.0, 20.0, 30.0, 40.0, 50.0]
        stats = data_analyzer.calculate_stats(data)
        self.assertEqual(stats["N"], 5)
        self.assertAlmostEqual(stats["Ortalama"], 30.0)
        self.assertAlmostEqual(stats["Medyan"], 30.0)
        self.assertAlmostEqual(stats["Min"], 10.0)
        self.assertAlmostEqual(stats["Max"], 50.0)
        self.assertAlmostEqual(stats["Standart Sapma"], 15.811388, places=4)

    def test_linear_regression(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        reg = data_analyzer.linear_regression(x, y)
        self.assertIsNotNone(reg)
        self.assertAlmostEqual(reg["egim (m)"], 2.0)
        self.assertAlmostEqual(reg["kesim (c)"], 0.0)
        self.assertAlmostEqual(reg["R_kare (R2)"], 1.0)

    def test_quadratic_regression(self):
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]  # y = x^2
        qreg = data_analyzer.quadratic_regression(x, y)
        self.assertIsNotNone(qreg)
        self.assertAlmostEqual(qreg["a (x^2)"], 1.0, places=4)
        self.assertAlmostEqual(qreg["b (x)"], 0.0, places=4)
        self.assertAlmostEqual(qreg["c (sabit)"], 0.0, places=4)

    def test_unit_conversions(self):
        self.assertAlmostEqual(data_analyzer.celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(data_analyzer.fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(data_analyzer.bar_to_psi(1.0), 14.5038, places=3)
        self.assertAlmostEqual(data_analyzer.psi_to_bar(14.5038), 1.0, places=3)
        self.assertAlmostEqual(data_analyzer.inch_to_mm(1.0), 25.4)
        self.assertAlmostEqual(data_analyzer.mm_to_inch(25.4), 1.0)
        self.assertAlmostEqual(data_analyzer.mps_to_kmh(10.0), 36.0)

    def test_cloud_cost_calculator(self):
        res, err = cloud_cost.estimate_cloud_cost(vcpu_count=4, ram_gb=16, storage_gb=200, egress_gb_month=50, running_hours_month=730)
        self.assertIsNone(err)
        self.assertGreater(res["Aylık On-Demand Maliyet ($)"], 0)
        self.assertGreater(res["Yıllık 1-Yıl Rezerv Tasarrufu ($)"], 0)
        self.assertGreater(res["Aylık Karbon Emisyonu (kg CO2e)"], 0)

    def test_sorting_and_binary_search(self):
        raw = [5, 2, 8, 1, 9]
        sorted_arr = algo_bench.bubble_sort(raw)
        self.assertEqual(sorted_arr, [1, 2, 5, 8, 9])
        self.assertEqual(algo_bench.binary_search(sorted_arr, 5), 2)
        self.assertEqual(algo_bench.binary_search(sorted_arr, 99), -1)

    def test_big_o_exponent_estimation(self):
        sizes = [100, 200, 400, 800]
        # T = c * N^2 sentetik veri
        times = [0.001 * (n**2) for n in sizes]
        beta = algo_bench.estimate_big_o_exponent(sizes, times)
        self.assertAlmostEqual(beta, 2.0, places=1)


class TestElectricalAndRoboticsTools(unittest.TestCase):
    def test_voltage_drop_3phase(self):
        res, err = electrical_calc.calculate_voltage_drop(voltage=400, current=30, length_m=100, section_mm2=10, material="bakir", system_type="3phase")
        self.assertIsNone(err)
        self.assertGreater(res["Gerilim Düşümü (V)"], 0)
        self.assertLess(res["Gerilim Düşümü Oranı (%)"], 5.0)

    def test_voltage_drop_1phase(self):
        res, err = electrical_calc.calculate_voltage_drop(voltage=230, current=16, length_m=30, section_mm2=2.5, material="bakir", system_type="1phase")
        self.assertIsNone(err)
        self.assertGreater(res["Gerilim Düşümü (V)"], 0)

    def test_filter_resonance(self):
        r = 1000.0
        c = 1e-6
        l = 0.1
        res = electrical_calc.calculate_filter_resonance(r, l, c)
        self.assertIn("RC Kesim Frekansı (Cutoff fc - Hz)", res)
        self.assertIn("RLC Rezonans Frekansı (f0 - Hz)", res)
        self.assertAlmostEqual(res["RLC Rezonans Frekansı (f0 - Hz)"], 503.29, delta=1.0)

    def test_power_factor_compensation(self):
        res, err = electrical_calc.calculate_power_factor_compensation(active_power_kw=100, current_cos_phi=0.75, target_cos_phi=0.98)
        self.assertIsNone(err)
        self.assertGreater(res["Gereken Kondansatör Gücü (kVAR)"], 0)
        self.assertGreater(res["Şebekeden Çekilen Güç Tasarrufu (kVA)"], 0)

    def test_modbus_simulator_scan(self):
        plc = modbus_sim.PLCSimulator()
        self.assertEqual(plc.coils[1], False)
        plc.coils[1] = True
        plc.scan_cycle()
        self.assertGreater(plc.input_registers[3003], 0)

    def test_modbus_emergency_stop(self):
        plc = modbus_sim.PLCSimulator()
        plc.coils[1] = True
        plc.scan_cycle()
        plc.discrete_inputs[101] = True
        plc.scan_cycle()
        self.assertEqual(plc.coils[1], False)
        self.assertEqual(plc.input_registers[3003], 0)
        self.assertEqual(plc.coils[3], True)

    def test_robotics_forward_and_inverse_kinematics(self):
        l1, l2 = 300.0, 200.0
        t1, t2 = 30.0, 45.0
        fk_res, err = robotics_calc.forward_kinematics_2r(l1, l2, t1, t2)
        self.assertIsNone(err)
        x_ee, y_ee = fk_res["Uç Nokta Konumu (X, Y - mm)"]
        
        # Ters kinematik ile geri çöz
        ik_res, err_ik = robotics_calc.inverse_kinematics_2r(l1, l2, x_ee, y_ee)
        self.assertIsNone(err_ik)
        c1 = ik_res["Çözüm 1 (Dirsek Aşağı / Elbow Down)"]
        self.assertAlmostEqual(c1["theta1 (deg)"], t1, delta=0.1)
        self.assertAlmostEqual(c1["theta2 (deg)"], t2, delta=0.1)

    def test_robotics_singularity(self):
        l1, l2 = 300.0, 200.0
        # theta2 = 0 derece tekilliktir
        jac_res = robotics_calc.calculate_robot_jacobian(l1, l2, 45.0, 0.0)
        self.assertIn("TEKİLLİK MEVCUT", jac_res["Kinematik Tekillik Durumu"])
        self.assertAlmostEqual(jac_res["Determinant det(J)"], 0.0)


class TestMechanicalAndCivilTools(unittest.TestCase):
    def test_gcode_generation(self):
        rect_gcode = gcode_gen.generate_rectangular_gcode(50, 80, -2, 5, 800, 3000, 6, "dummy.nc")
        self.assertIn("G21", rect_gcode)
        self.assertIn("M03 S3000", rect_gcode)
        self.assertIn("M30", rect_gcode)

        circ_gcode = gcode_gen.generate_circular_gcode(60, -2, 5, 600, 2500, 6, "dummy.nc")
        self.assertIn("G02", circ_gcode)

    def test_cpm_critical_path(self):
        tasks = {
            "A": cpm_calc.Task("A", 2, 2, 2, []),
            "B": cpm_calc.Task("B", 3, 3, 3, ["A"]),
            "C": cpm_calc.Task("C", 4, 4, 4, ["A"]),
            "D": cpm_calc.Task("D", 2, 2, 2, ["B", "C"])
        }
        topo_order, duration = cpm_calc.solve_cpm(tasks)
        self.assertIsNotNone(topo_order)
        critical_path = [u for u in topo_order if abs(tasks[u].slack) < 0.0001]
        self.assertEqual(critical_path, ["A", "C", "D"])
        self.assertAlmostEqual(duration, 8.0)

    def test_beam_mechanics(self):
        sec, err = beam_calc.calculate_section_properties("rectangle", b=50, h=100)
        self.assertIsNone(err)
        self.assertAlmostEqual(sec["Atalet Momenti Ix (mm⁴)"], (50 * 100**3) / 12.0)
        
        bm, err2 = beam_calc.calculate_beam_mechanics(1, 5000, 2.0, sec["Atalet Momenti Ix (mm⁴)"], sec["Mukavemet Momenti Wx (mm³)"], 210.0, 235.0)
        self.assertIsNone(err2)
        self.assertIn("Maksimum Eğilme Momenti", bm)
        self.assertIn("GÜVENLİ", bm["Gerilme Emniyeti"])

    def test_carnot_and_brayton_cycles(self):
        carnot_res, err = cycle_calc.calculate_carnot_efficiency(th_celsius=600, tc_celsius=25)
        self.assertIsNone(err)
        self.assertGreater(carnot_res["Maksimum Carnot Verimi η (%)"], 50.0)
        
        brayton_res, err_b = cycle_calc.calculate_brayton_cycle(pressure_ratio=12.0, t1_celsius=20, t3_celsius=1100)
        self.assertIsNone(err_b)
        self.assertGreater(brayton_res["Teorik Termal Verim η (%)"], 40.0)

    def test_otto_and_diesel_cycles(self):
        otto_res, err_o = cycle_calc.calculate_otto_cycle(compression_ratio=10.0)
        self.assertIsNone(err_o)
        self.assertGreater(otto_res["Otto Termal Verimi η (%)"], 55.0)
        
        diesel_res, err_d = cycle_calc.calculate_diesel_cycle(compression_ratio=18.0, cutoff_ratio=2.0)
        self.assertIsNone(err_d)
        self.assertGreater(diesel_res["Diesel Termal Verimi η (%)"], 55.0)


class TestChemicalProcessTools(unittest.TestCase):
    def test_pipe_friction_laminar(self):
        res, err = fluid_calc.calculate_pipe_friction(flow_rate_m3h=0.1, inner_dia_mm=50, pipe_length_m=10)
        self.assertIsNone(err)
        self.assertEqual(res["Akış Rejimi"], "Laminer Akış")
        self.assertAlmostEqual(res["Darcy Sürtünme Katsayısı (f)"], 64.0 / res["Reynolds Sayısı (Re)"], places=4)

    def test_pipe_friction_turbulent(self):
        res, err = fluid_calc.calculate_pipe_friction(flow_rate_m3h=20.0, inner_dia_mm=50, pipe_length_m=100)
        self.assertIsNone(err)
        self.assertEqual(res["Akış Rejimi"], "Türbülanslı Akış")
        self.assertGreater(res["Basınç Kaybı (Bar)"], 0)

    def test_heat_exchanger_lmtd(self):
        res, err = fluid_calc.calculate_heat_exchanger_lmtd(th_in=90, th_out=60, tc_in=20, tc_out=50, u_coeff=1000, flow_type="counter")
        self.assertIsNone(err)
        self.assertAlmostEqual(res["LMTD (°C)"], 40.0, places=2)

    def test_solution_dilution(self):
        res, err = fluid_calc.calculate_solution_dilution(c1=30, v1=10, c2=0, target_c=10)
        self.assertIsNone(err)
        self.assertAlmostEqual(res["Eklenmesi Gereken Çözücü Miktarı"], 20.0)


class TestAerospaceTools(unittest.TestCase):
    def test_isa_atmosphere(self):
        # Deniz seviyesi (0 m)
        res_sl, err = aero_calc.calculate_isa_atmosphere(0, velocity_kmh=360)
        self.assertIsNone(err)
        self.assertAlmostEqual(res_sl["Sıcaklık (°C)"], 15.0, places=1)
        self.assertAlmostEqual(res_sl["Basınç (Pascal)"], 101325.0, places=0)
        self.assertAlmostEqual(res_sl["Hava Yoğunluğu (kg/m³)"], 1.225, delta=0.01)
        # Mach ~ 100 m/s / 340.3 m/s ~ 0.29
        self.assertAlmostEqual(res_sl["Mach Sayısı (M)"], 0.294, delta=0.02)
        
        # 11000 m Tropopoz
        res_11k, _ = aero_calc.calculate_isa_atmosphere(11000)
        self.assertAlmostEqual(res_11k["Sıcaklık (°C)"], -56.5, delta=0.5)

    def test_naca_airfoil_coords(self):
        res, err = aero_calc.generate_naca_4digit("2412", num_points=21)
        self.assertIsNone(err)
        self.assertEqual(len(res["Ust Yuzey (Xu, Yu)"]), 21)
        self.assertAlmostEqual(res["Maksimum Kamburluk m (% chord)"], 2.0)
        self.assertAlmostEqual(res["Maksimum Kalınlık t (% chord)"], 12.0)

    def test_aerodynamic_lift_drag(self):
        res, err = aero_calc.calculate_aerodynamic_lift_drag(2*math.pi, alpha_deg=5.0, wing_area_m2=15.0, aspect_ratio=8.0, dynamic_pressure_pa=1000.0)
        self.assertIsNone(err)
        self.assertGreater(res["Taşıma Katsayısı (CL)"], 0)
        self.assertGreater(res["Toplam Taşıma Kuvveti (Lift - Newton)"], 0)
        self.assertGreater(res["Süzülme / Verim Oranı (L/D)"], 10.0)


class TestIndustrialQualityAndEnergyTools(unittest.TestCase):
    def test_oee_calculation(self):
        res, err = oee_calc.calculate_oee(planned_time=480, planned_down=30, unplanned_down=30, ideal_cycle=1.0, total_units=20000, reject_units=500)
        self.assertIsNone(err)
        self.assertGreater(res["OEE %"], 0)
        self.assertLessEqual(res["OEE %"], 100.0)

    def test_six_sigma_calculation(self):
        res, err = oee_calc.calculate_six_sigma(n_units=1000, opportunities=10, n_defects=34)
        self.assertIsNone(err)
        self.assertAlmostEqual(res["DPMO (Hata/Milyon Fırsat)"], 3400.0)
        self.assertGreater(res["Sigma Seviyesi (1.5 Shift dahil)"], 4.0)

    def test_takt_time(self):
        takt, err = oee_calc.calculate_takt_time(available_time_sec=28800, demand=720)
        self.assertIsNone(err)
        self.assertAlmostEqual(takt, 40.0)

    def test_carbon_footprint(self):
        res = carbon_calc.calculate_footprint(nat_gas=1000, diesel=500, petrol=200, electricity=5000, flight_km=10000, commute_km=20000)
        self.assertGreater(res["Toplam Karbon Ayak İzi tCO2e"], 0)
        self.assertGreater(res["Scope 1 (Doğrudan) tCO2e"], 0)
        self.assertGreater(res["Scope 2 (Dolaylı Enerji) tCO2e"], 0)
        self.assertGreater(res["Scope 3 (Diğer Dolaylı) tCO2e"], 0)

    def test_bess_sizing(self):
        res, err = bess_calc.calculate_bess_sizing(daily_consumption_kwh=20.0, autonomy_days=1.0, system_voltage_v=48.0, chemistry="lifepo4")
        self.assertIsNone(err)
        self.assertGreater(res["Gereken Nominal Depolama Kapasitesi (kWh)"], 20.0)
        self.assertGreater(res["Gereken Toplam Kapasite (Ah)"], 0)

    def test_lcos(self):
        res, err = bess_calc.calculate_lcos(capex_usd=10000, opex_annual_usd=150, nominal_kwh=25.0, chemistry="lifepo4")
        self.assertIsNone(err)
        self.assertGreater(res["Düzleştirilmiş Depolama Maliyeti (LCOS $/kWh)"], 0)


class TestAcousticsAndVibration(unittest.TestCase):
    def test_sdof_undamped(self):
        res, err = vib_calc.calculate_sdof_vibration(mass_kg=10.0, stiffness_n_m=1000.0, damping_c=0.0)
        self.assertIsNone(err)
        self.assertAlmostEqual(res["Doğal Açısal Frekans ωn (rad/s)"], 10.0)
        self.assertAlmostEqual(res["Doğal Frekans fn (Hz)"], 10.0 / (2.0 * math.pi))
        self.assertEqual(res["Sönüm Oranı (Zeta ζ)"], 0.0)
        self.assertIn("Sönümsüz", res["Sönüm Rejimi"])

    def test_sdof_underdamped_and_resonance(self):
        # m=50 kg, k=20000 N/m -> omega_n = 20 rad/s, fn ~ 3.183 Hz
        # c_critical = 2 * sqrt(20000 * 50) = 2 * 1000 = 2000 Ns/m
        # c = 100 -> zeta = 100 / 2000 = 0.05 (underdamped)
        res, err = vib_calc.calculate_sdof_vibration(mass_kg=50.0, stiffness_n_m=20000.0, damping_c=100.0, excitation_freq_hz=3.183)
        self.assertIsNone(err)
        self.assertAlmostEqual(res["Sönüm Oranı (Zeta ζ)"], 0.05, places=3)
        self.assertIn("Düşük Sönümlü", res["Sönüm Rejimi"])
        self.assertGreater(res["Dinamik Büyütme Faktörü (DMF / Q)"], 5.0)
        self.assertIn("TEHLİKELİ REZONANS", res["Rezonans Tehlikesi"])

    def test_acoustics_decibel_sum_and_distance(self):
        # 80 dB + 80 dB = 83.01 dB
        res = vib_calc.calculate_acoustics_decibels(sound_levels_db=[80.0, 80.0], r1_m=5.0, r2_m=10.0)
        self.assertAlmostEqual(res["Bileşke Toplam Gürültü Seviyesi (dB SPL)"], 83.0103, places=2)
        # Sınır 85 dBA altı
        self.assertIn("GÜVENLİ", res["İSG Gürültü Maruziyet Değerlendirmesi"])
        # Mesafe ikiye katlandığında 6 dB düşmeli
        self.assertIn("Uzaklaşma Sonucu (5.0 m -> 10.0 m)", res)


class TestEngineeringEconomics(unittest.TestCase):
    def test_npv_calculation(self):
        # Yatırım: 100000, Nakit akışı: [30000, 40000, 50000], %10 iskonto
        res, err = econ_calc.calculate_npv(100000, [30000, 40000, 50000], 0.10)
        self.assertIsNone(err)
        expected_pv = (30000 / 1.1) + (40000 / (1.1**2)) + (50000 / (1.1**3))
        expected_npv = expected_pv - 100000
        self.assertAlmostEqual(res["Net Mevcut Değer (NPV)"], expected_npv, places=2)

    def test_irr_calculation(self):
        # 100k yatırım, yılda 40k x 3 yıl -> IRR ~ 9.7%
        irr = econ_calc.calculate_irr(100000, [40000, 40000, 40000])
        self.assertIsNotNone(irr)
        # IRR ile NPV hesaplandığında sıfıra çok yakın olmalı
        npv_at_irr, _ = econ_calc.calculate_npv(100000, [40000, 40000, 40000], irr)
        self.assertAlmostEqual(npv_at_irr["Net Mevcut Değer (NPV)"], 0.0, delta=0.1)

    def test_payback_and_feasibility_analysis(self):
        c0 = 100000
        cfs = [30000, 40000, 50000]
        # Basit payback: 1. yılda 30k, 2. yılda 70k, 3. yılda 30k/50k = 0.6 yıl -> 2.6 yıl
        pb = econ_calc.calculate_payback_period(c0, cfs)
        self.assertAlmostEqual(pb, 2.6, places=2)
        
        analysis, err = econ_calc.analyze_capital_budgeting(c0, cfs, discount_rate=0.08)
        self.assertIsNone(err)
        self.assertGreater(analysis["Net Bugünkü Değer (NPV - $)"], 0)
        self.assertGreater(analysis["Yatırım Getirisi (ROI %)"], 0)
        self.assertGreater(analysis["Fayda / Maliyet Oranı (BCR)"], 1.0)
        self.assertIn("ONAYLANABİLİR", analysis["Nihai Yatırım Tavsiyesi"])


class TestWebDashboard(unittest.TestCase):
    def test_dashboard_components(self):
        web_mod = import_from_path("web_dashboard.py")
        self.assertIn("Engineering Tools - Web Dashboard", web_mod.HTML_PAGE)
        self.assertIn("calcBeam", web_mod.HTML_PAGE)
        self.assertIn("calcAero", web_mod.HTML_PAGE)
        self.assertIn("calcEcon", web_mod.HTML_PAGE)
        self.assertIn("calcVib", web_mod.HTML_PAGE)
        self.assertIsNotNone(web_mod.EngineeringServerHandler)


if __name__ == "__main__":
    unittest.main()
