import sys
import re
import matplotlib.pyplot as plt
import matplotlib

temp_iter_list = []
temp_vel_list = []
temp_p_list = []
temp_omega_list = []
temp_epsilon_list = []
temp_k_list = []
iter_list = []
velx_list = []
vely_list = []
velz_list = []
omega_list = []
epsilon_list = []
k_list = []

with open(sys.argv[1], 'r') as file:
    for line in file:
        time_string = (r'^Time\s=\s+(.*)')
        vel_string = (r'U(.*),\sInitial\sresidual\s=\s(\S+)')
        p_string = (r'p,\sInitial\sresidual\s=\s(\S+)')
        omega_string = (r'omega,\sInitial\sresidual\s=\s(\S+)')
        epsilon_string = (r'epsilon,\sInitial\sresidual\s=\s(\S+)')
        k_string = (r'k,\sInitial\sresidual\s=\s(\S+)')
        if re.findall(time_string,line): 
            temp_iter_list.append(re.findall(time_string,line))
        if re.findall(vel_string,line): 
            temp_vel_list.append(re.findall(vel_string,line))
        if re.findall(p_string,line): 
            temp_p_list.append(re.findall(p_string,line))
        if re.findall(omega_string,line): 
            temp_omega_list.append(re.findall(omega_string,line))
        if re.findall(epsilon_string,line): 
            temp_epsilon_list.append(re.findall(epsilon_string,line))
        if re.findall(k_string,line): 
            temp_k_list.append(re.findall(k_string,line))             

    iter_list = [float(x) for sublist in temp_iter_list for x in sublist]
    
    for tuple in temp_vel_list:
        if tuple[0][0] == 'x':
            velx_list.append(float(tuple[0][1].split(',')[0]))
        if tuple[0][0] == 'y':
            vely_list.append(float(tuple[0][1].split(',')[0]))
        if tuple[0][0] == 'z':
            velz_list.append(float(tuple[0][1].split(',')[0]))
    
    num = int(len(temp_p_list)/len(iter_list))
    p_list = temp_p_list[::num]
    p_list = [float(sublist[0].split(',')[0]) for sublist in p_list]

    omega_list = [float(sublist[0].split(',')[0]) for sublist in temp_omega_list]
    epsilon_list = [float(sublist[0].split(',')[0]) for sublist in temp_epsilon_list]
    k_list = [float(sublist[0].split(',')[0]) for sublist in temp_k_list]

    #print(f"Iterations: {iter_list}", f"\nUx: {velx_list}", f"\nUy: {vely_list}", f"\nUz: {velz_list}", f"\nPressure: {p_list}", f"\nOmega: {omega_list}", f"\nEpsilon: {epsilon_list}", f"\nk: {k_list}")

# Plot residuals

#Change font type and font size in axis labels
#matplotlib.rcParams.update({'legend.markerscale': 1.5, 'legend.handlelength': 1.5, 'legend.frameon': 1, 'legend.handletextpad': 1 , 'legend.framealpha': 1, 'font.size': 18,'font.family':'Times New Roman'})

#matplotlib.rcParams['text.usetex'] = True
#matplotlib.rcParams['text.latex.unicode'] = True
#matplotlib.rcParams['mathtext.fontset'] = 'stix'
#matplotlib.rcParams['font.family'] = 'STIXGeneral'

# Plot residuals
fig = plt.figure('Residuals')
plt.grid(False)

#Plot magU values
if velx_list:
    plt.plot(iter_list, velx_list, '-', color='black', label=r'$\bar{u}_x$', linewidth=0.7)
if vely_list:
    plt.plot(iter_list, vely_list, '-', color='red', label=r'$\bar{u}_y$', linewidth=0.7)
if velz_list:
    plt.plot(iter_list, velz_list, '-', color='green', label=r'$\bar{u}_z$', linewidth=0.7)

plt.plot(iter_list, p_list, '-', color='cyan', label=r'$p$', linewidth=0.7)

if omega_list:
    plt.plot(iter_list, omega_list, '-', color='violet', label=r'$\omega$', linewidth=0.7)
else:
    plt.plot(iter_list, epsilon_list, '-', color='violet', label=r'$\varepsilon$', linewidth=0.7)

plt.plot(iter_list, k_list, '-', color='orange', label=r'$k$', linewidth=0.7)

plt.xlabel(r'Iteration')#, fontsize=24)
plt.ylabel(r'Residual')#, fontsize=24)
plt.yscale("log")  
plt.xlim([0, len(iter_list)])
#plt.ylim([1e-10, 1])
#starty, endy = (1e-10, 1.01)
#startx, endx = (0, len(iter_list) + 0.01)
#plt.yticks(np.arange(starty,endy,1e-1))
#plt.xticks(np.arange(startx,endx,300))
#legend = plt.legend(numpoints=1, loc=0)
legend = plt.legend(ncol=2)
frame = legend.get_frame()
frame.set_facecolor('#ecf0f1')
frame.set_linewidth(0)

plt.show()

#Set figure size
#fig.set_size_inches(12, 8)

#When saving, specify the DPI
#plt.savefig('residuals.pdf', dpi = 250, bbox_inches='tight')