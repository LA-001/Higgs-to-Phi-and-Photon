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

#Set the RooModelConfig and let it know what the content of the workspace is about
model = ROOT.RooStats.ModelConfig()
model.SetWorkspace(f)
model.SetPdf("totPDF")

#Here we explicitly set the value of the parameters for the null hypothesis
#We want no signal contribution, so BR_H = 0
BR_H = f.var("BR_H")
poi = ROOT.RooArgSet(BR_H)
nullParams = poi.snapshot()
nullParams.setRealValue("BR_H",0.)

#Build the profile likelihood calculator
plc = ROOT.RooStats.ProfileLikelihoodCalculator()

plc.SetData(d.data("data"))
plc.SetModel(model)
plc.SetParameters(poi)
plc.SetNullParameters(nullParams)

#We get a HypoTestResult out of the calculator, and we can query it.
htr = plc.GetHypoTest()

print "-------------------------------------------------"
print "The p-value for the null is ", htr.NullPValue()
print "Corresponding to a signifcance of ", htr.Significance()
print "-------------------------------------------------"
