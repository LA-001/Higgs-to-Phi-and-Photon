import ROOT

fTot = ROOT.TFile("Tfile/tot_pdf.root")
tot = fTot.Get("ws_totPDF")

fData = ROOT.TFile("Tfile/data_gen.root")
d = fData.Get("ws_data")

scale_factor = d.var("scale_factor")

tot.var("lumi").setVal(40*pow(10,15)*scale_factor.getVal())
tot.var("Nbkg").setVal(586*scale_factor.getVal())

totPDF = tot.pdf("totPDF")
mesonGammaMass = d.var("mesonGammaMass")
data = d.data("data")

#fisso variabili
tot.var("alpha_L").setConstant(1)
tot.var("alpha_R").setConstant(1)
tot.var("n_L").setConstant(1)
tot.var("n_R").setConstant(1)
tot.var("sigma_L").setConstant(1)
tot.var("sigma_R").setConstant(1)

totPDF.fitTo(data)

xplot = mesonGammaMass.frame(50)
data.plotOn(xplot)
totPDF.plotOn(xplot)

canva = ROOT.TCanvas("Tot" , "Tot function" , 800 , 500)
canva.cd()
xplot.Draw()
canva.SaveAs("foto/fit_gen_1ab.png")
