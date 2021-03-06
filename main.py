import matplotlib.backend_bases
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.widgets import RadioButtons

## animations on or off?
animations = True

## set global variables
initial_scale = 1.0
sample_size = 200
movie_frame_size = 200
norm_dist_color ='red'
expo_dist_color ='green'
gamm_dist_color ='orange'
unif_dist_color ='blue'

fig = plt.figure(figsize=(7,5))
fig.suptitle('Compare probability distribution types', fontsize=16)
gspec = gridspec.GridSpec(ncols=3, nrows=2)

top_histogram = plt.subplot(gspec[0,1:])
current_histogram = plt.subplot(gspec[1, 0:1])
lower_right = plt.subplot(gspec[1,1:],sharex=top_histogram, sharey=current_histogram)

## the data
N = np.random.normal(0.0, scale=initial_scale, size=sample_size)
G = np.random.gamma(2, scale=initial_scale, size=sample_size)
E = np.random.exponential(scale=initial_scale, size=sample_size)
U = np.random.random(size=sample_size)
current_plot = N
current_color = norm_dist_color
current_plot_string = 'Normal'


def set_standard_dev(event):
    global N
    global G
    global E
    global U
    N = np.random.normal(0.0, scale=float(event), size=sample_size)
    G = np.random.gamma(2, scale=float(event), size=sample_size)
    E = np.random.exponential(scale=float(event), size=sample_size)
    U = np.random.random(size=sample_size)
    change_dist(current_plot_string)

def change_dist(event):
    global animations
    global current_plot
    global current_color
    global current_plot_string

    current_plot_string = event
    if event == 'Normal':
        current_plot=N
        current_color = norm_dist_color
    if event == 'Exponential':
        current_plot=E
        current_color = expo_dist_color
    if event == 'Gamma':
        current_plot=G
        current_color = gamm_dist_color
    if event == 'Uniform':
        current_plot=U
        current_color = unif_dist_color

    if (not animations):
        update_wo_anim()
    if (animations):
        a.frame_seq = a.new_frame_seq()

def update(i):

    if i == movie_frame_size:
        a.repeat
    #clear all existing frames
    top_histogram.cla()
    lower_right.cla()
    current_histogram.cla()

    # initialize graphs
    ## set up bins
    top_bins = np.arange(0,1,0.025)
    current_bins = np.arange(-4,4,.20)

    ## get the max hist height of each distribution for chart sizing
    hist_current, _ = np.histogram(current_plot, bins=current_bins)
    current_height = hist_current.max() + 0.5
    hist_uniform, _ = np.histogram(U,bins=top_bins)
    uniform_height = hist_uniform.max() + .05

    #### top histogram
    top_histogram.hist(U[:i], bins=top_bins, color='blue', alpha=0.6)
    top_histogram.set_ylim(0, uniform_height)
    top_histogram.set_xlabel('Uniform')
    top_histogram.xaxis.set_label_position('top')

    #### lower right histogram
    lower_right.scatter(U[:i], current_plot[:i])
    lower_right.set_xlabel('Intersection')

    #### lower left (CURRENT) histogram
    current_histogram.hist(current_plot[:i], bins=current_bins, orientation='horizontal', color=current_color, alpha=0.6)
    current_histogram.set_xlim(0, current_height)
    current_histogram.set_xlabel(current_plot_string)
    if (not current_histogram.xaxis_inverted()):
        current_histogram.invert_xaxis()
    lower_right.annotate('n = {}'.format(i), [0,-4])

def update_wo_anim():
    global N, E, G
    #clear all existing frames
    top_histogram.cla()
    lower_right.cla()
    current_histogram.cla()

    ## set up bins
    top_bins = np.arange(0,1,0.025)
    current_bins = np.arange(-4,4,.20)

    #### top histogram
    top_histogram.hist(U, bins=top_bins, color='blue', alpha=0.6)

    top_histogram.set_xlabel('Uniform')
    top_histogram.xaxis.set_label_position('top')

    #### lower right histogram
    lower_right.scatter(U, current_plot)
    lower_right.set_xlabel('Intersection')

    #### lower left (CURRENT) histogram
    current_histogram.hist(current_plot, bins=current_bins, orientation='horizontal', color=current_color, alpha=0.6)
    current_histogram.set_xlabel(current_plot_string)
    if (not current_histogram.xaxis_inverted()):
        current_histogram.invert_xaxis()

    if (not animations):
        plt.draw()

#radio buttons
ax_std_dev = plt.axes([0.205,0.47,0.15,0.3])
std_dev_button = RadioButtons(ax_std_dev, ['1.0','1.5','2.0','2.5'],active=0, activecolor='#ff10f0')
ax_std_dev.set_title('Scale')
for key,spine in ax_std_dev.spines.items():
    spine.set_visible(False)

ax_distribution_type = plt.axes([0.04,0.47,0.15,0.3])
ax_distribution_type.set_title('Type')
distribution_type_button = RadioButtons(ax_distribution_type, ['Normal','Gamma','Exponential','Uniform'],active=0, activecolor='#ff10f0')
for key,spine in ax_distribution_type.spines.items():
    spine.set_visible(False)

# display interactive content
distribution_type_button.on_clicked(lambda event: change_dist(event))
distribution_type_button.set_active(0)
std_dev_button.on_clicked(lambda event: set_standard_dev(event))
std_dev_button.set_active(0)


if (animations):
    a = animation.FuncAnimation(fig, update, interval=100, save_count=sample_size, repeat=True, frames=sample_size)
    a

# Need this for running in PyCharm
plt.show()