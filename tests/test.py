import btfd.plots as plots
import btfd.util as util

util.highchart_to_csv(plots.get_tweets('linx',300),'linx_tweets')

