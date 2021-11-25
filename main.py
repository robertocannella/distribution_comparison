import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.widgets import RadioButtons

## animations on or off?
animations = False

## set global variables
initial_scale = 1.0
sample_size = 200
movie_frame_size = 200
norm_dist_color ='red'
expo_dist_color ='green'
gamm_dist_color ='orange'



fig = plt.figure()
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

#radio buttons

ax_distribution_type = plt.axes([0.15,0.55,0.15,0.3])
distribution_type_button = RadioButtons(ax_distribution_type, ['Normal','Gamma','Exponential'], [True,False,False], activecolor='#ff10f0')
for key,spine in ax_distribution_type.spines.items():
    spine.set_visible(False)

distribution_type_button.on_clicked(lambda event: change_dist(event))

def change_dist(event):
    global current_plot
    global current_color
    if event == 'Normal':
        current_plot=N
        current_color = norm_dist_color
    if event == 'Exponential':
        current_plot=E
        current_color = expo_dist_color
    if event == 'Gamma':
        current_plot=G
        current_color = gamm_dist_color
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

    #### lower right histogram
    lower_right.scatter(U[:i], current_plot[:i])

    #### lower left (CURRENT) histogram
    current_histogram.hist(current_plot[:i], bins=current_bins, orientation='horizontal', color=current_color, alpha=0.6)
    current_histogram.set_xlim(0, current_height)
    if (not current_histogram.xaxis_inverted()):
        current_histogram.invert_xaxis()
    lower_right.annotate('n = {}'.format(i), [0,-4])

def update_wo_anim():
    #clear all existing frames
    top_histogram.cla()
    lower_right.cla()
    current_histogram.cla()

    ## set up bins
    top_bins = np.arange(0,1,0.025)
    current_bins = np.arange(-4,4,.20)

    #### top histogram
    top_histogram.hist(U, bins=top_bins, color='blue', alpha=0.6)

    #### lower right histogram
    lower_right.scatter(U, current_plot)

    #### lower left (CURRENT) histogram
    current_histogram.hist(current_plot, bins=current_bins, orientation='horizontal', color=current_color, alpha=0.6)
    if (not current_histogram.xaxis_inverted()):
        current_histogram.invert_xaxis()

# Generate animations
if (animations):
    a = animation.FuncAnimation(fig, update, interval=100, save_count=sample_size, repeat=True, frames=sample_size)
    a

# Need this for running in PyCharm
plt.show()