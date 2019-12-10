import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sqlite3
import math
import random 
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.formula.api import ols
from statsmodels.stats.power import tt_ind_solve_power
import seaborn as sns
sns.set(color_codes=True)


# Level Up: The notebook contains well-formatted, professional looking markdown cells explaining any substantial code. All functions have docstrings that act as professional-quality documentation.

class one_samp:

    def generate_samples(m1, s1, n1):
        """ create two random samples using the input parameters """
        sample1 = np.random.normal(loc= m1, scale=s1, size=n1)
        return sample1

    def cohens_d_one_samp(x, mu0):
        return (x.mean() - mu0) / x.std()   


    def ks_plot(data):

        plt.figure(figsize=(10, 7))
        plt.plot(np.sort(data), np.linspace(0, 1, len(data), endpoint=False))
        plt.plot(np.sort(stats.norm.rvs(loc=0, scale=3, size=len(data))), np.linspace(0, 1, len(data), endpoint=False))

        plt.legend(['ECDF', 'CDF'])
        plt.title('Comparing CDFs for K-S test, Sample size=' + str(len(data)))

class two_samp:

    def generate_samples(m1, s1, n1, m2, s2, n2):
        """ create two random samples using the input parameters """
        sample1 = np.random.normal(loc= m1, scale=s1, size=n1)
        sample2 = np.random.normal(loc= m2, scale=s2, size=n2)
        return sample1, sample2

    def cohens_d_two_samp(x,y):
        nx = len(x)
        ny = len(y)
        dof = nx + ny - 2
        return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.std(x, ddof=1) ** 2 + (ny-1)*np.std(y, ddof=1) ** 2) / dof)

    def welch_df(a, b):

        """ Calculate the effective degrees of freedom for two samples. """

        s1 = a.var(ddof=1) 
        s2 = b.var(ddof=1)
        n1 = a.size
        n2 = b.size

        numerator = (s1/n1 + s2/n2)**2
        denominator = (s1/ n1)**2/(n1 - 1) + (s2/ n2)**2/(n2 - 1)
        return numerator/denominator 

    def p_value(a, b, two_sided=False):
        """ calculate welch's ttest pvalue"""
        if two_sided == True:
            p = 1 - stats.t.cdf(welch_t(a, b),welch_df(a, b))
            return p*2
        else:
            p = 1 - stats.t.cdf(welch_t(a, b),welch_df(a, b))
            return p

    def welch_t(a, b):

        """ Calculate Welch's t-statistic for two samples. """
        numerator = a.mean() - b.mean()

        # “ddof = Delta Degrees of Freedom”: the divisor used in the calculation is N - ddof, 
        #  where N represents the number of elements. By default ddof is zero.

        denominator = np.sqrt(a.var(ddof=1)/a.size + b.var(ddof=1)/b.size)

        return np.abs(numerator/denominator)


    def ks_plot_2sample(data_1, data_2):
        '''
        Data entered must be the same size.
        '''
        length = len(data_1)
        plt.figure(figsize=(12, 7))
        plt.plot(np.sort(data_1), np.linspace(0, 1, len(data_1), endpoint=False))
        plt.plot(np.sort(data_2), np.linspace(0, 1, len(data_2), endpoint=False))
        plt.legend('top right')
        plt.legend(['Data_1', 'Data_2'])
        plt.title('Comparing 2 CDFs for KS-Test')

    def anova_table(data,target,feature):
        formula = '{} ~ C({})'.format(target,feature)
        lm = ols(formula, data).fit()
        table = sm.stats.anova_lm(lm, typ=2)
        return table

class sql:

    def tables(data):
        """ Data entered must be 'string' name or path to database """

        conn = sqlite3.Connection(data)
        cur = conn.cursor()

        cur.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type="table";
        """)
        print('tables from', data)
        return cur.fetchall()

    def preview(data,table):
        """ Returns first 5 row preview of specified table
            Data entered must be 'string' name or path to database
            Table 'name entered must be 'string'"""
        
        query = """
        SELECT * 
        FROM {}
        LIMIT 5
        """.format(table)
        conn = sqlite3.Connection(data)
        cur = conn.cursor()
        cur.execute(query)
        df = pd.DataFrame(cur.fetchall())
        df.columns = [x[0] for x in cur.description]
        print(table, 'from', data)
        return df


    def groupby(data, selection, table, column):
        """
        Returns data grouped by aggregation entered as selection
        All data must be entered as 'string'
        """
        
        query = """
        SELECT {}
        FROM {}
        GROUP BY {}

        """.format(selection,table,column)
        conn = sqlite3.Connection(data)
        cur = conn.cursor()
        cur.execute(query)
        df = pd.DataFrame(cur.fetchall())
        df.columns = [x[0] for x in cur.description]
        return df


    def boiler_plate():
        """
        Returns sql boiler plate query
        """
        print("""
        
        query = '''
        SELECT {}
        FROM {}
        WHERE {}

        '''
        conn = sqlite3.Connection(data)
        cur = conn.cursor()
        cur.execute(query)
        df = pd.DataFrame(cur.fetchall())
        df.columns = [x[0] for x in cur.description]
        df
        """)






