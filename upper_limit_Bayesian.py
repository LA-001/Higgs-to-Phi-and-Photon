import ROOT

fTot = ROOT.TFile("Tfile/tot_pdf.root")
f = fTot.Get("ws_totPDF")

fData = ROOT.TFile("Tfile/data_gen.root")
d = fData.Get("ws_data")

f.var("alpha_L").setConstant(1)
f.var("alpha_R").setConstant(1)
f.var("n_L").setConstant(1)
f.var("n_R").setConstant(1)
f.var("sigma_L").setConstant(1)
f.var("sigma_R").setConstant(1)

scale_factor = d.var("scale_factor")

f.var("lumi").setVal(40*pow(10,15)*scale_factor.getVal())
f.var("Nbkg").setVal(586*scale_factor.getVal())

#Configure the model, we need both the S+B and the B only models
sbModel = ROOT.RooStats.ModelConfig()
sbModel.SetWorkspace(f)
sbModel.SetPdf("totPDF")
sbModel.SetName("S+B Model")
poi = ROOT.RooArgSet(f.var("BR_H"))
poi.find("BR_H").setRange(0.,0.001)  #this is mostly for plotting
sbModel.SetParametersOfInterest(poi)

bModel = sbModel.Clone()
bModel.SetPdf("totPDF")
bModel.SetName( sbModel.GetName() + "_with_poi_0")
poi.find("BR_H").setVal(0)
bModel.SetSnapshot(poi)

#Example using the BayesianCalculator
#Now we also need to specify a prior in the ModelConfig
#To be quicker, we'll use the PDF factory facility of RooWorkspace
#Careful! For simplicity, we are using a flat prior, but this doesn't mean it's the best choice!
f.factory("Uniform::prior(BR_H)")
sbModel.SetPriorPdf(f.pdf("prior"))

#Construct the bayesian calculator
bc = ROOT.RooStats.BayesianCalculator(d.data("data"), sbModel)
bc.SetConfidenceLevel(0.95)
bc.SetLeftSideTailFraction(0.) # for upper limit

bcInterval = bc.GetInterval()

print "Bayesian upper limit on BR_H = ", bcInterval.UpperLimit()

bc_plot = bc.GetPosteriorPlot()

dataCanvas = ROOT.TCanvas("dataCanvas")
bc_plot.Draw()
dataCanvas.SaveAs("foto/upperLimit_Bayesian.png")
