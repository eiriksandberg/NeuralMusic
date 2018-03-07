import torch
from torch.autograd import Variable
import numpy as np
import torch.nn.functional as F
import torchvision
from torchvision import transforms
import torch.optim as optim
from torch import nn
import matplotlib.pyplot as plt
import processmidi as pm
import mido
import time
import sys
import os
sys.path.insert(0, '../postprocess/')
sys.path.insert(0, '../preprocess/')
import recreate
np.set_printoptions(threshold=np.nan)

class Normal(object):
    def __init__(self, mu, sigma, log_sigma, v=None, r=None):
        self.mu = mu
        self.sigma = sigma  # either stdev diagonal itself, or stdev diagonal from decomposition
        self.logsigma = log_sigma
        dim = mu.get_shape()
        if v is None:
            v = torch.FloatTensor(*dim)
        if r is None:
            r = torch.FloatTensor(*dim)
        self.v = v
        self.r = r


class Encoder(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        super(Encoder, self).__init__()
        self.LSTM = torch.nn.LSTM(D_in, H, 1, batch_first=True)
        self.linear1 = torch.nn.Linear(H, H)
        self.linear2 = torch.nn.Linear(H, D_out)

    def forward(self, x):
        output, hn = self.LSTM(x, None)
        #print(output)
        #print(hn)
        #exit()
        x = F.relu(self.linear1(output))
        return F.relu(self.linear2(x))


class Decoder(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        super(Decoder, self).__init__()
        self.LSTM = torch.nn.LSTM(D_in, H, 1, batch_first=True)
        self.linear1 = torch.nn.Linear(H,  H)
        self.linear2 = torch.nn.Linear(H, D_out)

    def forward(self, prev, z, hidden):
        #print("Decoder")
        #print(z)
        #exit()
        inp = torch.cat((prev, z), dim=2)
        #print(inp)
        #print(hidden)
        output, hn = self.LSTM(inp, hidden)
        #print(hn)
        #exit()
        #print(hn)
        #print(output)
        #exit()
        x = F.relu(self.linear1(output.squeeze(0)))
        return F.relu(self.linear2(x)), hn


class VAE(torch.nn.Module):

    def __init__(self, encoder, decoder, hidden_size, latent_dim):
        super(VAE, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self._enc_mu = torch.nn.Linear(hidden_size, latent_dim)
        self._enc_log_sigma = torch.nn.Linear(hidden_size, latent_dim)

    def _sample_latent(self, h_enc):
        """
        Return the latent normal sample z ~ N(mu, sigma^2)
        """
        mu = self._enc_mu(h_enc)
        log_sigma = self._enc_log_sigma(h_enc)
        sigma = torch.exp(log_sigma)
        std_z = torch.from_numpy(np.random.normal(0, 1, size=sigma.size())).float()

        self.z_mean = mu
        self.z_sigma = sigma

        return mu + sigma * Variable(std_z, requires_grad=False)  # Reparameterization trick

    def forward(self, state, criterion, input_dim, latent_dim, z_size, song_length):
        h_enc = self.encoder(state)
        #print(state)
        #exit()
        #print(h_enc)
        #exit()
        z = self._sample_latent(h_enc)
        #print(z)
        #exit()
        z = z.view(1, latent_dim, z_size) # Change the first 1 if more that one batch
        output = Variable(torch.zeros(1, 1, input_dim))
        song = None
        hidden = (z, z)
        temp_loss = None
        for i in range(0, song_length):
            output, hidden = self.decoder(output, z, hidden)
            state_i = state.squeeze(0)[i].view(1, input_dim)
            if song is None:
                song = output
                temp_loss = criterion(output, state_i)
            else:
                song = torch.cat((song, output), dim=0)
                temp_loss += criterion(output, state_i)
                #print("################")
                #print(state_i.topk(2))
                #print(output.topk(2))
                #exit()
            output = state_i  # test teacher forcing
            output = output.view(1, 1, input_dim)
        #return song.view(1, 128, 130)
        #exit()
        return temp_loss/song_length
        # expects 1x128x130


def latent_loss(z_mean, z_stddev):
    mean_sq = z_mean * z_mean
    stddev_sq = z_stddev * z_stddev
    return 0.5 * torch.mean(mean_sq + stddev_sq - torch.log(stddev_sq) - 1)


if __name__ == '__main__':
    t0 = time.time()
    '''Input data config'''
    directory = 'data'
    songdata = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            currentSong = np.loadtxt(directory+'/'+filename)
            currentSong = currentSong[1:129] # Making song shorter
            songdata.append(currentSong)
        else:
            print("Error while loading data. Could not find .txt files")
            exit()
    input_dim = 130 # 128 = 8 bars, 130 is midi notes, hold and pause
    batch_size = 1
    song_length = 128

    dataloader = torch.utils.data.DataLoader(songdata, batch_size=batch_size,
                                             shuffle=False, num_workers=2)

    hidden_size = 100
    z_size = 128
    latent_dim = 1

    print('Number of samples: ', len(songdata))
    encoder = Encoder(input_dim, hidden_size, hidden_size)
    decoder = Decoder(input_dim + z_size, z_size, input_dim)
    vae = VAE(encoder, decoder, hidden_size, latent_dim)

    criterion = nn.MSELoss()

    optimizer = optim.Adam(vae.parameters(), lr=0.0001)
    #optimizer = optim.Adam(vae.parameters(), lr=0.01)
    l = None
    for epoch in range(100):
        for i, data in enumerate(dataloader, 0):
            inputs = Variable(data).float()
            #inputs = Variable(inputs.resize_(batch_size, input_dim))
            optimizer.zero_grad()
            loss = vae(inputs, criterion, input_dim, latent_dim, z_size, song_length)
            ll = latent_loss(vae.z_mean, vae.z_sigma)
            loss = loss + ll # excluding ll for now
            loss.backward()
            optimizer.step()
            l = loss.data[0]
        print(epoch, l)
    t1 = time.time()

    #exit()

    sample = Variable(torch.randn(1, 1, 128))
    #s = vae.encoder(Variable(torch.randn(1, 128, 130)))
    #sample = vae._sample_latent(s)
    #sample = sample.view(1, 1, 128)
    output = Variable(torch.zeros(1, 1, 130))

    song = None
    hidden = (sample, sample)
    for i in range(0, 128):
        output, hidden = vae.decoder(output, sample, hidden)
        if song is None:
            song = output
        else:
            song = torch.cat((song, output), dim=0)
        output = output.view(1, 1, 130)
    #output = song.view(1, 128, 130)
    output = song
    #print(output)
    #exit()
    song = None
    for data in output:
        value, index = torch.max(data, 0)
        index = index.data[0]
        b = np.zeros(shape=(1, 130))

        '''Get highest probability'''
        '''
        if (index == 129):
            topKValue, topKIndex = torch.topk(data, 2)
            b.itemset((0, topKIndex.data[0]), 1)
            b.itemset((0, topKIndex.data[1]), 1)
        elif (index == 128):
            topKValue, topKIndex = torch.topk(data, 2)
            b.itemset((0, topKIndex.data[1]), 1)
        else:
            b.itemset((0, index), 1)
            print(index)
            #exit()
        '''

        ''' Monte Carlo Sampling'''
        value = data.multinomial(1)
        b.itemset((0, value.data[0]), 1)
        if (song is None):
            song = b
        else:
            song = np.concatenate([song, b])
    rec = recreate.RecreateMIDI()
    #print(song)
    track = rec.recreateMIDI(song, 30)
    rec.createMIDITest(track, 'VAERecreated')


    print('Runtime: ' + str(t1-t0) + " seconds")
    #plt.imshow(vae(inputs).data[0].numpy().reshape(1, 130), cmap='gray')
    #plt.show(block=True)
