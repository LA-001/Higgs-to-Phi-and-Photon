import ROOT

fTot = ROOT.TFile("Tfile/tot_pdf.root")
tot = fTot.Get("ws_tot")

totPDF = tot.pdf("totPDF")
mesonGammaMass = tot.var("mesonGammaMass")
data = tot.data("data")

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
#canva.SaveAs("foto/fit_gen_3ab.png")
