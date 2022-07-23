import sys, re
import matplotlib.pyplot as plt
import matplotlib
from prettytable import PrettyTable

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

pt = PrettyTable()

matplotlib.rcParams['text.usetex'] = True
fig = plt.figure('Residuals')
plt.grid(True)

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
    pt.add_column('Iteration', iter_list)

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

if velx_list:
    plt.plot(iter_list, velx_list, '-', color='black', label=r'$\bar{u}_x$', linewidth=0.7)
    pt.add_column('Velocity Ux', velx_list)
if vely_list:
    plt.plot(iter_list, vely_list, '-', color='red', label=r'$\bar{u}_y$', linewidth=0.7)
    pt.add_column('Velocity Uy', vely_list)
if velz_list:
    plt.plot(iter_list, velz_list, '-', color='green', label=r'$\bar{u}_z$', linewidth=0.7)
    pt.add_column('Velocity Uz', velz_list)
if p_list:
    plt.plot(iter_list, p_list, '-', color='cyan', label=r'$p$', linewidth=0.7)
    pt.add_column('Pressure p', p_list)
if omega_list:
    plt.plot(iter_list, omega_list, '-', color='violet', label=r'$\omega$', linewidth=0.7)
    pt.add_column('Spec. diss. rate omega', omega_list)
else:
    plt.plot(iter_list, epsilon_list, '-', color='violet', label=r'$\varepsilon$', linewidth=0.7)
    pt.add_column('Diss. rate epsilon', epsilon_list)
if k_list:
    plt.plot(iter_list, k_list, '-', color='orange', label=r'$k$', linewidth=0.7)
    pt.add_column('Turb. kin. energy', k_list)

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

if len(sys.argv) > 2:
    for arg in sys.argv:
        if arg == '--print-residual-values':
            print(pt)
        if arg == '-h':
            print('\nDescription\n\n-h\tHelp.\n--print-residual-values\tPlot residual values in the form of table.\n')

plt.show()