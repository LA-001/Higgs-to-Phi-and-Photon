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

#First example is with a frequentist approach
fc = ROOT.RooStats.FrequentistCalculator(d.data("data"), bModel, sbModel)
fc.SetToys(2500,1500)

#Create hypotest inverter passing the desired calculator 
calc = ROOT.RooStats.HypoTestInverter(fc)

#set confidence level (e.g. 95% upper limits)
calc.SetConfidenceLevel(0.95)

#use CLs
calc.UseCLs(1)

#reduce the noise
calc.SetVerbose(0)

#Configure ToyMC Sampler
toymcs = calc.GetHypoTestCalculator().GetTestStatSampler()

#Use profile likelihood as test statistics 
profll = ROOT.RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())

#for CLs (bounded intervals) use one-sided profile likelihood
profll.SetOneSided(1)

#set the test statistic to use for toys
toymcs.SetTestStatistic(profll)

npoints = 10 #Number of points to scan
# min and max for the scan (better to choose smaller intervals)
poimin = poi.find("BR_H").getMin()
poimax = poi.find("BR_H").getMax()

print "Doing a fixed scan  in interval : ", poimin, " , ", poimax
calc.SetFixedScan(npoints,poimin,poimax);

result = calc.GetInterval() #This is a HypoTestInveter class object
upperLimit = result.UpperLimit()

#Now let's print the result of the two methods
#First the CLs
print "################"
print "The observed CLs upper limit is: ", upperLimit

#Compute expected limit
print "Expected upper limits, using the B (alternate) model : "
print " expected limit (median) ", result.GetExpectedUpperLimit(0)
print " expected limit (-1 sig) ", result.GetExpectedUpperLimit(-1)
print " expected limit (+1 sig) ", result.GetExpectedUpperLimit(1)
print "################"

freq_plot = ROOT.RooStats.HypoTestInverterPlot("HTI_Result_Plot","Frequentist scan result for psi xsec",result)

canva = ROOT.TCanvas("dataCanvas")
freq_plot.Draw()
dataCanvas.SaveAs("foto/upperLimit_CLs.png")
