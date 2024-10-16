import ROOT

space = ROOT.TFile("Tfile/ws.root")
ws = space.Get("ws")

ws.Print()

ws.var("alpha_L").setConstant(1)
ws.var("alpha_R").setConstant(1)
ws.var("n_L").setConstant(1)
ws.var("n_R").setConstant(1)
ws.var("sigma_L").setConstant(1)
ws.var("sigma_R").setConstant(1)

scale_factor = ws.var("scale_factor")

ws.var("lumi").setVal(40*pow(10,15)*scale_factor.getVal())
ws.var("Nbkg").setVal(586*scale_factor.getVal())

sbModel = ROOT.RooStats.ModelConfig()
sbModel.SetWorkspace(ws)
sbModel.SetPdf("totPDF")
sbModel.SetName("S+B Model")

poi = ROOT.RooArgSet(ws.var("BR_H"))
sbModel.SetParametersOfInterest(poi)

bModel = sbModel.Clone()
bModel.SetPdf("totPDF")
bModel.SetName("S+B model_with_poi_0")
poi.find("BR_H").setVal(0)
bModel.SetSnapshot(poi)

fc = ROOT.RooStats.FrequentistCalculator(ws.data("data"), bModel,sbModel)
fc.SetToys(1000,1000)

toymcs = fc.GetTestStatSampler()

profll = ROOT.RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())
profll.SetOneSided(1)

toymcs.SetTestStatistic(profll)

calc = ROOT.RooStats.HypoTestInverter(fc)

calc.SetConfidenceLevel(0.95)

calc.UseCLs(1)

calc.SetVerbose(0)

npoints = 10
poimin = 0.00035
poimax = 0.00075

print("doing a fixed scan in interval:", poimin, ",", poimax)
calc.SetFixedScan(npoints,poimin,poimax);

result = calc.GetInterval()
upperLimit = result.UpperLimit()

print("################")
print("The CLs upper limit osservato is:", upperLimit)

print("Expected upper limits, using the B (alternate) model : ")
print(" expected limit (median) ", result.GetExpectedUpperLimit(0))
print(" expected limit (-1 sig) ", result.GetExpectedUpperLimit(-1))
print(" expected limit (+1 sig) ", result.GetExpectedUpperLimit(1))
print("################")

plot = ROOT.RooStats.HypoTestInverterPlot("HTI_Result_Plot","Frequentist scan result for BR H)",result)
canva = ROOT.TCanvas("canva")
plot.Draw()
canva.SaveAs("foto/canva_UP.png")
