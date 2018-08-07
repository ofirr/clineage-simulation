clear;
clc;

load('matlab_ampli1_xL.mat')

assert( size(xL, 1) == 1 );
assert( size(xL, 2) == 600 );

Dropout.P = xL(1:100);
Dropout.Q = xL(101:end);

save('allelic_dropout_prob.mat', 'Dropout');
