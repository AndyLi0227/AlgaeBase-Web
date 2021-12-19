import logging, os

import torch

from torchvision import transforms, datasets
from torch.utils.data import DataLoader, RandomSampler, DistributedSampler, SequentialSampler, Dataset, distributed

#from train import train
from PIL import Image


logger = logging.getLogger(__name__)


def get_loader(args):
    if args.local_rank not in [-1, 0]:
        torch.distributed.barrier()

    transform_train = transforms.Compose([
        transforms.RandomResizedCrop((args.img_size, args.img_size), scale=(0.05, 1.0)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])
    transform_test = transforms.Compose([
        transforms.Resize((args.img_size, args.img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

    if args.dataset == "cifar10":
        trainset = datasets.CIFAR10(root="./data",
                                    train=True,
                                    download=True,
                                    transform=transform_train)
        testset = datasets.CIFAR10(root="./data",
                                   train=False,
                                   download=True,
                                   transform=transform_test) if args.local_rank in [-1, 0] else None

    else:
        trainset = datasets.CIFAR100(root="./data",
                                     train=True,
                                     download=True,
                                     transform=transform_train)
        testset = datasets.CIFAR100(root="./data",
                                    train=False,
                                    download=True,
                                    transform=transform_test) if args.local_rank in [-1, 0] else None
    if args.local_rank == 0:
        torch.distributed.barrier()

    train_sampler = RandomSampler(trainset) if args.local_rank == -1 else DistributedSampler(trainset)
    test_sampler = SequentialSampler(testset)
    train_loader = DataLoader(trainset,
                              sampler=train_sampler,
                              batch_size=args.train_batch_size,
                              num_workers=4,
                              pin_memory=True)
    test_loader = DataLoader(testset,
                             sampler=test_sampler,
                             batch_size=args.eval_batch_size,
                             num_workers=4,
                             pin_memory=True) if testset is not None else None

    return train_loader, test_loader

class TheDs(Dataset):
    def __init__(self, file_lst, dir, train_or_pred, transform = None):
        self.file_lst = file_lst
        self.dir = dir
        self.train_or_pred = train_or_pred
        self.transform = transform
        # if self.train_or_pred != "predict":
        #     if 'yes' in self.file_lst:
        #         self.label = 1
        #     else:
        #         self.label = 0
    
    def __len__(self):
        return len(self.file_lst)
    
    def __getitem__(self, idx):
        img = Image.open(os.path.join(self.dir, self.file_lst[idx])).convert('RGB')
        label = 1 if 'yes' in self.file_lst[idx] else 0
        if self.train_or_pred != "predict" and self.transform:
            img = self.transform(img)
            return img, label
        else:
            img = self.transform(img)
            return img, self.file_lst[idx]

def TheDataLoader(args, ds):
    data_loader = DataLoader(ds,
                            batch_size=args.train_batch_size,
                            shuffle=True)
    return data_loader
