import torch
import torch.nn as nn
import torch.nn.functional as F


def conv3x3(in_planes, out_planes, stride=1):
	"""3x3 convolution with padding"""
	return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
					 padding=1, bias=False)


class BasicBlock(nn.Module):
	expansion = 1

	def __init__(self, inplanes, planes, stride=1, downsample=None):
		super(BasicBlock, self).__init__()
		self.conv1 = conv3x3(inplanes, planes, stride)
		self.bn1 = nn.BatchNorm2d(planes, eps=1e-05)
		self.relu = nn.ReLU(inplace=True)
		self.conv2 = conv3x3(planes, planes)
		self.bn2 = nn.BatchNorm2d(planes, eps=1e-05)
		self.downsample = downsample
		self.stride = stride

	def forward(self, x):
		residual = x

		out = self.conv1(x)
		out = self.bn1(out)
		out = self.relu(out)

		out = self.conv2(out)
		out = self.bn2(out)

		if self.downsample is not None:
			residual = self.downsample(x)

		out += residual
		out = self.relu(out)

		return out


class ResNetConv4(nn.Module):

	def __init__(self, init_weight_path):
		
		self.inplanes = 64
		super(ResNetConv4, self).__init__()
		self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3,
							   bias=False)
		self.bn1 = nn.BatchNorm2d(64, eps=1e-05)
		self.relu = nn.ReLU(inplace=True)
		self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
		self.layer1 = self._make_layer(BasicBlock, 64, 2)
		self.layer2 = self._make_layer(BasicBlock, 128, 2, stride=2)
		self.layer3 = self._make_layer(BasicBlock, 256, 2, stride=2)
		if init_weight_path : 
			msg = 'Loading weight from {}'.format(init_weight_path)
			print (msg)
			self.init_weight(init_weight_path)
			
		
		
	def _make_layer(self, block, planes, blocks, stride=1):
		downsample = None
		if stride != 1 or self.inplanes != planes * block.expansion:
			downsample = nn.Sequential(
				nn.Conv2d(self.inplanes, planes * block.expansion,
						  kernel_size=1, stride=stride, bias=False),
				nn.BatchNorm2d(planes * block.expansion, eps=1e-05),
			)

		layers = []
		layers.append(block(self.inplanes, planes, stride, downsample))
		self.inplanes = planes * block.expansion
		for i in range(1, blocks):
			layers.append(block(self.inplanes, planes, 1, None))

		return nn.Sequential(*layers)
		
	def init_weight(self, init_weight_path) :
		model_params=torch.load(init_weight_path)
		for key in list(model_params.keys()) : 
			if 'layer4' in key : 
				model_params.pop(key, None)
		
		model_params.pop('fc.bias', None)
		model_params.pop('fc.weight', None)
		self.load_state_dict(model_params)
		
		
	def resume(self, load_model_path) : 
		self.load_state_dict( torch.load(load_model_path) )
	
	def trainFreezeBN(self):
		"""
		Training with freeze BN
		"""
		print("Freezing Mean/Var of BatchNorm2D.")
		print("Freezing Weight/Bias of BatchNorm2D.")
		for m in self.modules():
			if isinstance(m, nn.BatchNorm2d):
				m.eval()
				m.weight.requires_grad = False
				m.bias.requires_grad = False
				
	def forward(self, x):
		x = self.conv1(x)
		x = self.bn1(x)
		x = self.relu(x)
		x = self.maxpool(x)

		x = self.layer1(x)
		x = self.layer2(x)
		x = self.layer3(x)
		
		return x
		
		
class ResNetConv5(nn.Module):

	def __init__(self, init_weight_path):
		
		self.inplanes = 64
		super(ResNetConv5, self).__init__()
		self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3,
							   bias=False)
		self.bn1 = nn.BatchNorm2d(64, eps=1e-05)
		self.relu = nn.ReLU(inplace=True)
		self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
		self.layer1 = self._make_layer(BasicBlock, 64, 2)
		self.layer2 = self._make_layer(BasicBlock, 128, 2, stride=2)
		self.layer3 = self._make_layer(BasicBlock, 256, 2, stride=2)
		self.layer4 = self._make_layer(BasicBlock, 512, 2, stride=2)
		if init_weight_path : 
			msg = 'Loading weight from {}'.format(init_weight_path)
			print (msg)
			self.init_weight(init_weight_path)
			
		
		
	def _make_layer(self, block, planes, blocks, stride=1):
		downsample = None
		if stride != 1 or self.inplanes != planes * block.expansion:
			downsample = nn.Sequential(
				nn.Conv2d(self.inplanes, planes * block.expansion,
						  kernel_size=1, stride=stride, bias=False),
				nn.BatchNorm2d(planes * block.expansion, eps=1e-05),
			)

		layers = []
		layers.append(block(self.inplanes, planes, stride, downsample))
		self.inplanes = planes * block.expansion
		for i in range(1, blocks):
			layers.append(block(self.inplanes, planes, 1, None))

		return nn.Sequential(*layers)
		
	def init_weight(self, init_weight_path) :
		model_params=torch.load(init_weight_path)
		
		model_params.pop('fc.bias', None)
		model_params.pop('fc.weight', None)
		self.load_state_dict(model_params)
		
		
	def resume(self, load_model_path) : 
		self.load_state_dict( torch.load(load_model_path) )
	
	def trainFreezeBN(self):
		"""
		Training with freeze BN
		"""
		print("Freezing Mean/Var of BatchNorm2D.")
		print("Freezing Weight/Bias of BatchNorm2D.")
		for m in self.modules():
			if isinstance(m, nn.BatchNorm2d):
				m.eval()
				m.weight.requires_grad = False
				m.bias.requires_grad = False
				
	def forward(self, x):
		x = self.conv1(x)
		x = self.bn1(x)
		x = self.relu(x)
		x = self.maxpool(x)

		x = self.layer1(x)
		x = self.layer2(x)
		x = self.layer3(x)
		x = self.layer4(x)
		
		return x
		



	


	
	
	

	
