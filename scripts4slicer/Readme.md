## What has been done before
For patients before 039, the registration is done as follows (Let's call it Reg 1 for short.):
- apply `(in_dwi_b50)_to_(in_3d).tfm` by hardening the transform 
- apply `(in_3d)_to_(ex_xd).tfm` by using brainsresample module

For patients 039 onwards, the registration is done in a different way (Let's call it Reg 2 for short.):
- apply `(in_dwi_b50)_to_(in_3d).tfm` by using brainsresample module
- apply `(in_3d)_to_(ex_xd).tfm` by using brainsresample module

## What should be done
The best way to do it is using Reg 1 where the first registration is applied by 'hardening the transform'. The benefit of this approach is that the data is not resampled when the transform is applied, however it is resampled when the brains resample module is applied. This means Reg 2 gives data that looked more 'smoothed' than Reg 1, because data has been resampled twice rather than once. 
