# QUICK START GUIDE
## Atmospheric Water Harvesting Suite

**NanoBio Studio | Bio Catalyst Engineering**

---

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies
```bash
cd d:\AquaCatalyst Designer\awh_suite
pip install -r requirements.txt
```

### Step 2: Launch the App
```bash
streamlit run main.py
```

### Step 3: Open in Browser
```
http://localhost:8501
```

---

## 📖 First Use: Try a Preset

1. Open app → Click "Load Preset" in sidebar
2. Select "Chitosan/Silica/ZnO" (beginner-friendly)
3. Click through tabs 1-8 to understand the workflow
4. Play with sliders and "Calculate/Run" buttons
5. Download reports in Tab 8

---

## 💡 What to Try First

### Quick Design (5 minutes)
1. Tab 2: Keep default feedstock, synthesis route
2. Tab 3: Click "Calculate Membrane Properties"
3. Tab 5: Run "Simulator" with default conditions
4. Tab 8: Download technical report

### Deep Dive (30 minutes)
1. Tab 2: Experiment with different feedstocks + synthesis routes
2. Tab 3: Adjust nanoparticle loading, layer config
3. Tab 4: Modify device geometry (diameter, height)
4. Tab 5: Try different RH and temperature scenarios
5. Tab 6: Compare against benchmarks
6. Tab 7: See cost impact of design changes
7. Tab 8: Export all results

### Optimization Challenge (1 hour)
- Goal: Maximize water yield while minimizing cost
- Tab 2-4: Iterate feedstock → membrane → device
- Tab 5: Check performance
- Tab 6: Rank against competitors
- Tab 7: See cost-benefit tradeoff
- Find your Pareto-optimal design!

---

## 🎯 Key Navigation

| Tab | What to Do | Key Button |
|-----|-----------|-----------|
| 1 - Overview | Understand system | Read info |
| 2 - Feedstock | Select materials | Estimate Properties |
| 3 - Membrane | Design formulation | Calculate Membrane |
| 4 - Device | Configure prototype | Calculate Geometry |
| 5 - Simulator | Predict performance | Run Simulation |
| 6 - Benchmarking | Compare systems | Auto-populated |
| 7 - Cost | Analyze economics | Calculate Costs |
| 8 - Reports | Export results | Generate + Download |

---

## 📊 Understanding Results

### Key Metrics to Watch

**Water Yield (L/kg/day)**
- 0.1-0.3: Limited (bench phase)
- 0.3-0.5: Good (pilot-worthy)
- 0.5+: Excellent (commercially viable)

**Adsorption Score (0-1)**
- > 0.8: Strong moisture capture
- 0.6-0.8: Moderate
- < 0.6: Needs optimization

**Cost per Liter ($)**
- < $5: Competitive
- $5-15: Reasonable for early stage
- > $15: Needs cost reduction

**Sustainability Score (0-1)**
- > 0.8: Excellent green design
- 0.6-0.8: Good
- < 0.6: Consider greener alternatives

---

## ⚙️ Customizing Your Design

### To Improve Water Yield
✅ Increase nanoparticle loading (Tab 3, up to 15%)
✅ Use dual-layer design (Tab 3)
✅ Enable thermal assist (Tab 4)
✅ Simulate at higher RH (Tab 5, 60-80%)
✅ Increase device surface area (Tab 4, bigger diameter)

### To Reduce Cost
✅ Choose cheaper feedstock (Tab 2, rice husk <$2/kg)
✅ Simplify membrane (Tab 3, single layer, <10% loading)
✅ Smaller prototype device (Tab 4, < 30 cm diameter)
✅ Reduce manufacturing complexity (Tab 7)

### To Improve Sustainability
✅ Use agro-waste feedstocks (Tab 2)
✅ Green synthesis routes (Tab 2, green synthesis option)
✅ Biodegradable polymers (Tab 3, chitosan)
✅ Passive design (Tab 4, no thermal assist)

---

## 💾 Saving Your Work

### Auto-Save
- Project saved in Streamlit session (while app runs)
- Close/reopen = start fresh

### Manual Save (Recommended)
- Tab 8 → "Download JSON"
- Save to computer
- Load later by copying JSON into app memory

### Export Formats
- **JSON**: For saving/loading projects
- **CSV**: Spreadsheet analysis
- **TXT**: Reports for stakeholders
- **SOP**: Draft manufacturing procedure

---

## 🔍 Troubleshooting

### "Simulation gave me zero water yield"
→ Membrane adsorption too low?
- Tab 3: Increase hydrophilicity (add silica or ZnO)
- Tab 5: Increase RH (currently too dry?)
- Check thermal mode supports desorption

### "Cost is unrealistically high"
→ Check nanoparticle loading & synthesis complexity
- Tab 2: Switch to simpler synthesis route
- Tab 3: Reduce nanoparticle loading to <10%
- Tab 7: Check if "Pre-commercial" scale is too aggressive

### "Device has warnings"
→ Review Tab 4 validation messages
- "Cone angle unusual" → Keep 45-70°
- "Funnel throat too large" → < 1/4 device diameter
- "Stability issues" → Add more support columns

### "Numbers don't match my experiments"
→ This is a design tool, not calibrated to your data yet
- Use results as guidance, not predictions
- Adjust heuristic parameters based on your validation data
- See README for extending the module

---

## 🎓 Educational Mode

Want to understand the science?

1. **Tab 1**: Read system overview
2. **Tab 2**: Learn about green synthesis routes
3. **Tab 3**: Understand membrane physics
4. **Tab 4**: Study device geometry
5. **Tab 5**: See heuristic calculation process
6. **Tab 6**: Compare against published benchmarks
7. **Tab 7**: Economics of scale-up
8. **Tab 8**: Generate full technical report

→ Use Tab 8's technical summary as learning document

---

## 🚀 For Investors/Stakeholders

### Executive Summary (10 min)
1. Tab 1: Overview ("Purpose" section)
2. Tab 8: "Generate Investor Summary"
3. Download + send to stakeholders

### Full Technical Presentation (30 min)
1. Tab 1: System overview
2. Tab 3-4: Design choices
3. Tab 5-6: Performance demo
4. Tab 7: Economic viability
5. Tab 8: Export technical summary + SOP

### Investment Readiness Checklist
- [ ] Tab 6: Competitive vs. MOF systems? ✅ Better cost/sustainability
- [ ] Tab 5: Water yield promising? ✅ 0.3+ L/kg/day
- [ ] Tab 7: Cost per liter viable? ✅ < $10
- [ ] Sustainability strong? ✅ > 0.8 score
- [ ] Manufacturability feasible? ✅ > 0.6 score
- [ ] TRL advanced enough? ✅ Check Tab 1

---

## 🔬 For R&D Teams

### Experimental Validation Protocol

1. **Design phase** (Week 1)
   - Use this tool to define target specifications
   - Tab 2-4: Lock down feedstock, synthesis, device
   - Tab 8: Export SOP draft

2. **Synthesis phase** (Week 2-3)
   - Follow Tab 8's SOP draft
   - Characterize nanoparticles (XRD, SEM, BET)
   - Compare actual vs. predicted properties (Tab 2)

3. **Formulation phase** (Week 3-4)
   - Synthesize membrane per Tab 3 design
   - Measure contact angle, adsorption isotherms
   - Validate Tab 3 predictions

4. **Prototype phase** (Week 4-5)
   - Build device per Tab 4 design
   - Run bench-scale experiments
   - Log actual water yields

5. **Comparison phase** (Week 5-6)
   - Compare experimental vs. Tab 5 predictions
   - Refine heuristic parameters if systematic error
   - Use Tab 6 benchmarks to assess vs. literature

6. **Optimization phase** (Ongoing)
   - Use validated design to optimize
   - Iterate design → simulation → experiment

---

## 📞 Need Help?

### Check These First
1. Tab 1 → "About This Module" section
2. README.md in awh_suite folder
3. Hover tooltips (ℹ️ icons in app)

### Common Questions

**Q: Is this a certified engineering tool?**
A: No, it's design-stage guidance. Validate with experiments.

**Q: Can I use this for commercial product?**
A: Use results to guide R&D. Require proper engineering + testing before commercialization.

**Q: How accurate are the yield predictions?**
A: ±50% order-of-magnitude in early stages. Refine with experimental data.

**Q: Can I add my own benchmarks?**
A: Yes, see README.md "Extending the Module"

**Q: What's the best starting design?**
A: Use "Chitosan/Silica/ZnO" preset → Tab 5 simulator → iterate

---

## 🎉 You're Ready!

1. **Launch** the app (see Step 2 above)
2. **Load a preset** to get comfortable
3. **Try the workflow** (Overview → Feedstock → ... → Reports)
4. **Download your first report** ✅
5. **Start designing your own system** 🚀

---

**Questions?** See README.md or raise an issue in repository.

**Happy designing!**

*NanoBio Studio | Bio Catalyst Engineering | 2026*
