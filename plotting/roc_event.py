import sys
sys.path.append('..')
from utils.TrainingUtils import *
import h5py
import time

#fin = "../data/BB_v2_3500_images/BB_images_testset.h5"
#fin = "../data/BB_v2_2500_images/BB_images_testset.h5"
fin = "../data/BB_UL_MC_small_v2_deta_images/"
time_start = time.time()
batch_start = 20
batch_stop = 30
sig_idx = 1
#roc_plot_name = "s%i_event_roc_cwola_all_kfold_qt.png" % sig_idx
#sic_plot_name = "s%i_event_sic_cwola_all_kfold_qt.png" % sig_idx
roc_plot_name = "s%i_event_roc_ae_latent_cmp.png" % sig_idx
sic_plot_name = "s%i_event_sic_ae_latent_cmp.png" % sig_idx
m_low = 2250.
m_high = 2750.
#m_low = 3150.
#m_high = 3850.

no_minor_bkgs = True

d_eta = 1.3


single_file = True
hadronic_only = True

sic_max = 10

plot_dir = "../plots/dec1_ae_eta_dep/"
model_dir = "../models/AEs/nov29/"

#plot_dir = "../runs/cwola_40spb_fullrun/"
#model_dir = "../runs/cwola_40spb_fullrun/"


f_models = [
"all_latent4_4batch.h5",
"all_4batch.h5",
"all_latent8_4batch.h5",
"all_latent10_4batch.h5",
#"all_8batch.h5",
#"deta_4batch.h5",
#"deta_8batch.h5",
#"deta_nov29_8batch.h5",
#"deta_nov29_24batch.h5",
#"{j_label}_autoencoder_m3500.h5", 
#"july22/{j_label}_deta_sig00_TNT0_seed1_s3.h5",
#"july22/{j_label}_deta_sig00_TNT0_seed2_s3.h5",
#"july22/{j_label}_deta_sig00_TNT0_seed3_s3.h5",
#"july22/{j_label}_deta_sig00_TNT0_seed4_s3.h5",
#"july22/{j_label}_deta_sig00_TNT0_seed5_s3.h5",

#"july21/{j_label}_cwola_ensemble_eff_cut_num_model5_seed1/",
#"july21/{j_label}_cwola_ensemble_eff_cut_num_model5_seed2/",
#"july21/{j_label}_cwola_ensemble_eff_cut_num_model5_seed3/",
#"july21/{j_label}_cwola_ensemble_eff_cut_num_model5_seed4/",
#"july21/{j_label}_cwola_ensemble_eff_cut_num_model5_seed5/",

#"july22/jrand_v2_deta_sig025_TNT0_seed1_s{sig_idx}.h5",
#"july22/jrand_v2_deta_sig025_TNT0_seed2_s{sig_idx}.h5",
#"july22/jrand_v2_deta_sig025_TNT0_seed3_s{sig_idx}.h5",
#"july22/jrand_v2_deta_sig025_TNT0_seed4_s{sig_idx}.h5",
#"july22/jrand_v2_deta_sig025_TNT0_seed5_s{sig_idx}.h5",

#"aug18/jrand_v2_deta_sig01_TNT0_seed1_s{sig_idx}.h5",
#"aug18/jrand_v2_deta_sig01_TNT0_seed2_s{sig_idx}.h5",
#"aug18/jrand_v2_deta_sig01_TNT0_seed3_s{sig_idx}.h5",
#"aug18/jrand_v2_deta_sig01_TNT0_seed4_s{sig_idx}.h5",
#"aug18/jrand_v2_deta_sig01_TNT0_seed5_s{sig_idx}.h5",

#"{j_label}_kfold0/",
#"{j_label}_kfold1/",
#"{j_label}_kfold2/",
#"{j_label}_kfold3/",
#"{j_label}_kfold4/",

#"aug18/jrand_v2_xval5_ensemble_sig01_seed1/",
#"aug18/jrand_v2_xval5_ensemble_sig01_seed2/",
#"aug18/jrand_v2_xval5_ensemble_sig01_seed3/",
#"aug18/jrand_v2_xval5_ensemble_sig01_seed4/",
#"aug18/jrand_v2_xval5_ensemble_sig01_seed5/",
]

labels = [
         "AE Latent Size 4",
         "AE Latent Size 6",
         "AE Latent Size 8",
         "AE Latent Size 10",
#         "AE 8 batch (dEta cut, rotated images)",
#         "AE 24 batch (dEta cut, rotated images)",
#         "AE 4 batch",
#         "AE 8 batch",
#         "AE 4 batch (dEta cut)",
#         "AE 8 batch (dEta cut)",
        ]




#model types: 0 CNN (one jet), 1 auto encoder, 2 dense (one jet), 3 CNN (both jets), 4 dense (both jets), 5 is VAE 
model_type = [1,1,1,1,1,1]
num_models = [1,1,1,1,1,1]
rand_sort = [False, False, False, False, False, False]

#f_models = ["autoencoder_m3500.h5",  "mar2/dense_sig10_TNT1_s%i.h5", "mar2/cwola_hunting_dense_sig10_s%i.h5"]
#f_models = ["autoencoder_m3500.h5",  "mar15_deta/dense_deta_sig025_TNT1_s%i.h5", "mar15_deta/cwola_hunting_dense_deta_sig025_s%i.h5"]
#labels = ["Autoencoder ", "TNT (S/B = 0.25%)", "CWoLa (S/B = 0.25%)"]
#model_type = [1, 2, 2] 

#f_models = ["autoencoder_m2500.h5",  "mar2/dense_sig10_TNT1_s%i.h5", "mar2/cwola_hunting_dense_sig10_s%i.h5"]
#labels = ["Autoencoder ", "TNT (S/B = 1%)", "CWoLa (S/B = 1%)"]
#model_type = [1, 2, 2] 

colors = ["g", "b", "r", "gray", "purple", "pink", "orange", "m", "skyblue", "yellow"]

n_points = 200.

logy= True

need_images = 1 in model_type

if(need_images):
    keys = ["j1_images", "j2_images", "jj_images", "j1_features", "j2_features", "jj_features", 'jet_kinematics']
else:
    keys = ["j1_features", "j2_features", "jj_features", 'jet_kinematics']


if(single_file):
    num_data = -1
    data_start = 0
    data = DataReader(fin=fin, sig_idx = sig_idx, data_start = data_start, data_stop = data_start + num_data, keys = keys, keep_mlow = m_low, keep_mhigh = m_high, 
            hadronic_only = hadronic_only, deta = deta, batch_start = batch_start, batch_stop = batch_stop, no_minor_bkgs = no_minor_bkgs )
    data.read()
    j1_dense_inputs = data['j1_features']
    j2_dense_inputs = data['j2_features']
    jj_dense_inputs = data['jj_features']

    j1_images = j2_images = jj_images = None
    if(need_images):
        j1_images = data['j1_images']
        j2_images = data['j2_images']
        jj_images = data['jj_images']
    Y = data['label'].reshape(-1)

else:
    bkg_start = 1000000
    n_bkg = 400000
    sig_start = 20000
    sig_stop = -1
    d_bkg = DataReader(f_bkg, keys = keys, signal_idx = -1, start = bkg_start, stop = bkg_start + n_bkg, m_low = m_low, m_high = m_high, hadronic_only = hadronic_only, eta_cut = eta_cut )
    d_bkg.read()
    d_sig = DataReader(f_sig, keys = keys, signal_idx = -1, start = sig_start, stop = sig_stop, m_low = m_low, m_high = m_high, hadronic_only = hadronic_only, eta_cut = eta_cut )
    d_sig.read()

    j1_im_bkg = d_bkg['j1_images']
    j1_im_sig = d_sig['j1_images']
    j1_images = np.concatenate((j1_im_bkg, j1_im_sig), axis = 0)

    j2_im_bkg = d_bkg['j2_images']
    j2_im_sig = d_sig['j2_images']
    j2_images = np.concatenate((j2_im_bkg, j2_im_sig), axis = 0)

    jj_im_bkg = d_bkg['jj_images']
    jj_im_sig = d_sig['jj_images']
    jj_images = np.concatenate((jj_im_bkg, jj_im_sig), axis = 0)

    Y = np.concatenate((np.zeros(j1_im_bkg.shape[0], dtype=np.int8), np.ones(j1_im_sig.shape[0], dtype=np.int8)))


if(any(rand_sort)):
    swapping_idxs = np.random.choice(a=[True,False], size = Y.shape[0])
    j1rand_images = copy.deepcopy(j1_images)
    j2rand_images = copy.deepcopy(j2_images)
    j1rand_images[swapping_idxs] = j2_images[swapping_idxs]
    j2rand_images[swapping_idxs] = j1_images[swapping_idxs]

    j1rand_dense_inputs = copy.deepcopy(j1_dense_inputs)
    j2rand_dense_inputs = copy.deepcopy(j2_dense_inputs)
    j1rand_dense_inputs[swapping_idxs] = j2_dense_inputs[swapping_idxs]
    j2rand_dense_inputs[swapping_idxs] = j1_dense_inputs[swapping_idxs]
else:
    j1rand_images = j2rand_images = j1rand_dense_inputs = j2rand_dense_inputs = None



# reading images
#filter signal

sig_effs = []
bkg_effs = []
aucs = []
sics = []
for idx,f in enumerate(f_models):
    if('sig_idx' in f): 
        f = f.format(sig_idx = sig_idx)
    print(idx, f, model_type[idx])
    if(model_type[idx]  <= 2 or model_type[idx] == 5): #classifier on each jet

        if(rand_sort[idx]):
            j1_score, j2_score = get_jet_scores(model_dir, f, model_type[idx], j1rand_images, j2rand_images, j1rand_dense_inputs, j2rand_dense_inputs, num_models = num_models[idx])
        else:
            j1_score, j2_score = get_jet_scores(model_dir, f, model_type[idx], j1_images, j2_images, j1_dense_inputs, j2_dense_inputs, num_models = num_models [idx])
        Y = Y.reshape(-1)
        j1_qs = quantile_transform(j1_score.reshape(-1,1)).reshape(-1)
        j2_qs = quantile_transform(j2_score.reshape(-1,1)).reshape(-1)
        #sig_eff = np.array([len(Y[(j1_score > np.percentile(j1_score,i)) & (j2_score > np.percentile(j2_score,i)) & (Y==1)])/len(Y[Y==1]) for i in np.arange(0.,100., 100./n_points)])
        #bkg_eff = np.array([len(Y[(j1_score > np.percentile(j1_score,i)) & (j2_score > np.percentile(j2_score,i)) & (Y==0)])/len(Y[Y==0]) for i in np.arange(0.,100., 100./n_points)])
        sig_eff = np.array([(Y[(j1_qs > perc) & (j2_qs > perc) & (Y==1)].shape[0])/(Y[Y==1].shape[0]) for perc in np.arange(0.,1., 1./n_points)])
        bkg_eff = np.array([(Y[(j1_qs > perc) & (j2_qs > perc) & (Y==0)].shape[0])/(Y[Y==0].shape[0]) for perc in np.arange(0.,1., 1./n_points)])
        sig_eff = np.clip(sig_eff, 1e-8, 1.)
        bkg_eff = np.clip(bkg_eff, 1e-8, 1.)

        #print('bkg eff 10% ',f,np.percentile(j1_score,10),np.percentile(j2_score,10),bkg_eff[11])
        sig_effs.append(sig_eff)
        bkg_effs.append(bkg_eff)
        sics.append(sig_eff/np.sqrt(bkg_eff))
        aucs.append(auc(bkg_eff, sig_eff))


    else:
        jj_scores = get_jj_scores(model_dir, model_name[idx], model_type[idx], jj_images, jj_dense_inputs)
        bkg_eff, sig_eff, thresholds_cwola = roc_curve(Y, jj_scores)
        sig_effs.append(sig_eff)
        bkg_effs.append(bkg_eff)
        sics.append(sig_eff/np.sqrt(bkg_eff))
        aucs.append(auc(bkg_eff, sig_eff))


            


fs = 18
fs_leg = 14

#roc curve
plt.figure(figsize=fig_size)
for i in range(len(labels)):
    if(logy):
        temp = np.array(bkg_effs[i])
        #guard against division by 0
        temp = np.clip(temp, 1e-8, 1.)
        ys = 1./temp
    else:
        ys = bkg_effs[i]
    plt.plot(sig_effs[i], ys, lw=2, color=colors[i], label=labels[i] + (" (AUC = %.3f)" % aucs[i]))
#plt.plot(fpr_cwola, tpr_cwola, lw=2, color="purple", label="CWOLA = %.3f" %(auc_cwola))
#plt.plot(tnt_bkg_eff, tnt_sig_eff, lw=2, color="r", label="TNT Dense = %.3f"%(auc(tnt_bkg_eff,tnt_sig_eff)))
#plt.plot(sup_bkg_eff, sup_sig_eff, lw=2, color="g", label="Sup. Dense = %.3f"%(auc(sup_bkg_eff,sup_sig_eff)))
#plt.plot(ae_bkg_eff, ae_sig_eff, lw=2, color="b", label="Autoencoders = %.3f"%(auc(ae_bkg_eff,ae_sig_eff)))

#plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='k', label='random chance')
plt.xlim([0, 1.0])
plt.xlabel('Signal Efficiency', fontsize = fs)
if(logy):
    plt.ylim([1., 1e4])
    plt.yscale('log')
    plt.ylabel('QCD Rejection Rate', fontsize = fs)
else:
    plt.ylim([0, 1.0])
    plt.ylabel('Background Efficiency')
plt.tick_params(axis='x', labelsize=fs_leg)
plt.tick_params(axis='y', labelsize=fs_leg)
plt.legend(loc="upper left", fontsize= fs_leg)
plt.savefig(plot_dir+roc_plot_name)
print("Saving file to %s " % (plot_dir + roc_plot_name))

#sic curve
eff_min = 1e-3
plt.figure(figsize=fig_size)
for i in range(len(labels)):
    mask_ = bkg_effs[i] > eff_min
    print(labels[i], aucs[i], np.amax(sics[i][mask_]))
    plt.plot(bkg_effs[i][mask_], sics[i][mask_], lw=2, color=colors[i], label=labels[i] + (" (AUC = %.3f)" % aucs[i]))
#plt.plot(fpr_cwola, tpr_cwola, lw=2, color="purple", label="CWOLA = %.3f" %(auc_cwola))
#plt.plot(tnt_bkg_eff, tnt_sig_eff, lw=2, color="r", label="TNT Dense = %.3f"%(auc(tnt_bkg_eff,tnt_sig_eff)))
#plt.plot(sup_bkg_eff, sup_sig_eff, lw=2, color="g", label="Sup. Dense = %.3f"%(auc(sup_bkg_eff,sup_sig_eff)))
#plt.plot(ae_bkg_eff, ae_sig_eff, lw=2, color="b", label="Autoencoders = %.3f"%(auc(ae_bkg_eff,ae_sig_eff)))

#plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='k', label='random chance')
plt.xlim([eff_min, 1.0])
if(sic_max > 0):
    plt.ylim([0,sic_max])
plt.xscale('log')
plt.xlabel('Background Efficiency', fontsize = fs)
plt.ylabel('Significance Improvement', fontsize = fs)
plt.tick_params(axis='x', labelsize=fs_leg)
plt.tick_params(axis='y', labelsize=fs_leg)
plt.grid(axis = 'y', linestyle='--', linewidth = 0.5)
plt.legend(loc="best", fontsize= fs_leg)
plt.savefig(plot_dir+sic_plot_name)
print("Saving file to %s " % (plot_dir + sic_plot_name))

time_done = time.time()

print("Took %s" % (time_done - time_start))

del data


