'''
ParIO 
Python module to do Par file IO
'''
class ParIO(object):
    def __init__(self, fname = "test.par"):
        self.name_pars = [] # parameters
        self.val_pars  = [] # values
        self.uncer_pars= [] # uncertainities
        self.flag_pars = [] # FIT flags
        self.npars = 0 # number of parameters
        self.pulsar_name = '' # name of the pulsar
        self.everything_else = '' # everything that goes in par file
        #
        foo = open(fname,"r") # input file
        self.tpar = open(".temp_par_file","w+") # temporary par file
        # copyign foo --> tpar 
        # we will only change tpar
        self.cf = foo.read() # read all the lines
        self.tpar.write(self.cf)  # write all the lines
        self.tpar.flush()    # just to check
        ## Parsing
        self.__parser__()
        ## Close original input file
        foo.close()

    def __parser__(self):
        '''
        Parsing PAR file
        '''
        self.tpar.seek(0) # moving it to start
        xl = self.tpar.readline() # reading one file
        #TODO: Assuming PAR file starts with PSRJ
        xxl = map(str,xl.split())
        self.pulsar_name = xxl[1]
        xl = self.tpar.readline()
        while xl != str(""):
            # until empty string is not reached
            x1 = map(str,xl.split())
            if len(x1) == 4:
                # TODO: check 1/0 flag to see if user wants to fit
                # Logic to escape T2*
                if x1[0] == "T2EFAC" or x1[0] == "T2EQUAD":
                    self.everything_else += xl 
                    # self.everything_else += '\n'
                    pass
                else:
                    # book keeping logic
                    self.name_pars.append(x1[0])
                    self.val_pars.append(x1[1])
                    self.flag_pars.append(x1[2])
                    self.uncer_pars.append(x1[3])
                    self.npars += 1
            else:
                self.everything_else += xl 
            # self.everything_else += '\n'
            xl = self.tpar.readline()

    def updateParams(self,names,vals):
        '''
        Receives list of names and values
        updates the temp par file accordingly
        '''
        # sanity check
        if len(names) != len(vals):
            raise AttributeError('The input to updateParam is crazy.')
        # this is why Python is cool
        for pname, pval in zip(names,vals):
            pidx = self.name_pars.index(pname) 
            # finds the index in name_pars
            self.val_pars[pidx] = pval
        # write it to file
        self.__update_temp_par__()

    def __update_temp_par__(self):
        '''
        Writes `those` four lists to `temp` par file
        '''
        # clearing the file first
        self.tpar.seek(0) # bring to top
        self.tpar.truncate(0) # clearing content
        # first PSRJ
        self.tpar.write('PSRJ ' + self.pulsar_name + ' \n')
        # second the PARs
        for pname, pval, pflag, punc in zip(self.name_pars, self.val_pars, self.flag_pars, self.uncer_pars):
            self.tpar.write(str(pname) + ' ' + \
                    str(pval) + ' ' + \
                    str(pflag) + ' ' + \
                    str(punc) + ' ' + '\n')
        # third and last everything else
        self.tpar.write(self.everything_else)
        self.tpar.flush()
if __name__ == "__main__":
    # running from terminal
    # testing
    cf = ParIO()
    print "The number of parameters parsed is {}".format(cf.npars)
    print "The name of the pulsar is {}".format(cf.pulsar_name)
    cf.updateParams(['F0','DM'],['100.000','200.000'])
