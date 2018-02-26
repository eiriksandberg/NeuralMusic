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
sys.path.insert(0, '../postprocess/')
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
        self.linear1 = torch.nn.Linear(D_in, H)
        self.linear2 = torch.nn.Linear(H, D_out)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        return F.relu(self.linear2(x))


class Decoder(torch.nn.Module):
    def __init__(self, D_in, H, D_out):
        super(Decoder, self).__init__()
        self.linear1 = torch.nn.Linear(D_in, H)
        self.linear2 = torch.nn.Linear(H, D_out)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        return F.relu(self.linear2(x))


class VAE(torch.nn.Module):
    latent_dim = 65

    def __init__(self, encoder, decoder):
        super(VAE, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self._enc_mu = torch.nn.Linear(100, 65)
        self._enc_log_sigma = torch.nn.Linear(100, 65)

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

    def forward(self, state):
        h_enc = self.encoder(state)
        z = self._sample_latent(h_enc)
        global zett
        zett = z
        return self.decoder(z)


def latent_loss(z_mean, z_stddev):
    mean_sq = z_mean * z_mean
    stddev_sq = z_stddev * z_stddev
    return 0.5 * torch.mean(mean_sq + stddev_sq - torch.log(stddev_sq) - 1)


if __name__ == '__main__':
    t0 = time.time()
    songdata = np.loadtxt('littlered.txt')
    songdata = songdata[1:129]

    input_dim = 130 # 128 = 8 bars, 130 is midi notes, hold and pause
    batch_size = 1

    dataloader = torch.utils.data.DataLoader(songdata, batch_size=batch_size,
                                             shuffle=False, num_workers=2)

    print('Number of samples: ', len(songdata))

    encoder = Encoder(input_dim, 100, 100)
    decoder = Decoder(65, 100, input_dim)
    vae = VAE(encoder, decoder)

    criterion = nn.MSELoss()

    optimizer = optim.Adam(vae.parameters(), lr=0.0001)
    l = None
    for epoch in range(100):
        for i, data in enumerate(dataloader, 0):
            inputs = Variable(data).float()
            #inputs = Variable(inputs.resize_(batch_size, input_dim))
            optimizer.zero_grad()
            dec = vae(inputs)
            ll = latent_loss(vae.z_mean, vae.z_sigma)
            loss = criterion(dec, inputs) + ll
            loss.backward()
            optimizer.step()
            l = loss.data[0]
        print(epoch, l)
    t1 = time.time()

    sample = Variable(torch.randn(100, 65))
    output = vae.decoder(sample)
    song = None
    for data in output:
        value, index = torch.max(data, 0)
        index = index.data[0]
        b = np.zeros(shape=(1, 130))
        if (index == 129):
            topKValue, topKIndex = torch.topk(data, 2)
            b.itemset((0, topKIndex.data[0]), 1)
            b.itemset((0, topKIndex.data[1]), 1)
        else:
            b.itemset((0, index), 1)
        if (song is None):
            song = b
        else:
            song = np.concatenate([song, b])
    print(song)
    rec = recreate.RecreateMIDI()
    track = rec.recreateMIDI(song, 30)
    rec.createMIDITest(track, 'VAERecreated')


    print('Runtime: ' + str(t1-t0) + " seconds")
    #plt.imshow(vae(inputs).data[0].numpy().reshape(1, 130), cmap='gray')
    #plt.show(block=True)
