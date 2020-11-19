
from ...node import StartNode, HiddenNode, EndNode
from ...layers import BaseModel, Conv2D, ELU, MaxPooling, Concat, BatchNormalization, \
                      Conv2D_Transpose

class UNetPlusPlus(BaseModel):

    @BaseModel.init_name_scope
    def __init__(self, nclass):
        '''
        define a UNet++ model object.
        Paper: https://arxiv.org/abs/1807.10165

        Args:
            nclass (integer): The number of classes of the ouput mask.
        '''

        def _encode_block(in_hn, out_ch):
            blk = []
            blk.append(MaxPooling(poolsize=(2,2), stride=(2,2), padding='VALID'))
            blk.append(Conv2D(num_filters=out_ch, kernel_size=(3,3), stride=(1,1), padding='SAME'))
            blk.append(ELU())
            blk.append(BatchNormalization())
            blk.append(Conv2D(num_filters=out_ch, kernel_size=(3,3), stride=(1,1), padding='SAME'))
            blk.append(ELU())
            blk.append(BatchNormalization())
            out_hn = HiddenNode(prev=[in_hn], layers=blk)
            return out_hn

        def _merge_decode_block(deblk_hn, blk_hn, in_ch, out_ch):
            deblk = []
            deblk.append(Conv2D_Transpose(num_filters=in_ch, kernel_size=(2,2), stride=(2,2), padding='SAME'))

            blk = []
            blk.append(Conv2D(num_filters=out_ch, kernel_size=(3,3), stride=(1,1), padding='SAME'))
            blk.append(ELU())
            blk.append(BatchNormalization())
            blk.append(Conv2D(num_filters=out_ch, kernel_size=(3,3), stride=(1,1), padding='SAME'))
            blk.append(ELU())
            blk.append(BatchNormalization())

            deblk_hn = HiddenNode(prev=[deblk_hn], layers=deblk)
            out_hn = HiddenNode(prev=[deblk_hn] + blk_hn,
                                   input_merge_mode=Concat(axis=-1),
                                   layers=blk)
            return out_hn

        # encoding
        blk0 = []
        blk0.append(Conv2D(num_filters=32, kernel_size=(3,3), stride=(1,1), padding='SAME'))
        blk0.append(ELU())
        blk0.append(BatchNormalization())
        blk0.append(Conv2D(num_filters=32, kernel_size=(3,3), stride=(1,1), padding='SAME'))
        blk0.append(ELU())
        blk0.append(BatchNormalization())

        self.startnode = StartNode(input_vars=[None])
        blk00_hn = HiddenNode(prev=[self.startnode], layers=blk0)
        blk10_hn = _encode_block(blk00_hn, out_ch=64)
        blk20_hn = _encode_block(blk10_hn, out_ch=128)
        blk30_hn = _encode_block(blk20_hn, out_ch=256)
        blk40_hn = _encode_block(blk30_hn, out_ch=512)

        # decoding
        blk31_hn = _merge_decode_block(blk40_hn, [blk30_hn], in_ch=512, out_ch=256)

        blk21_hn = _merge_decode_block(blk30_hn, [blk20_hn], in_ch=256, out_ch=128)
        blk22_hn = _merge_decode_block(blk31_hn, [blk20_hn, blk21_hn], in_ch=256, out_ch=128)

        blk11_hn = _merge_decode_block(blk20_hn, [blk10_hn], in_ch=128, out_ch=64)
        blk12_hn = _merge_decode_block(blk21_hn, [blk10_hn, blk11_hn], in_ch=128, out_ch=64)
        blk13_hn = _merge_decode_block(blk22_hn, [blk10_hn, blk11_hn, blk12_hn], in_ch=128, out_ch=64)

        blk01_hn = _merge_decode_block(blk10_hn, [blk00_hn], in_ch=64, out_ch=32)
        blk02_hn = _merge_decode_block(blk11_hn, [blk00_hn, blk01_hn], in_ch=64, out_ch=32)
        blk03_hn = _merge_decode_block(blk12_hn, [blk00_hn, blk01_hn, blk02_hn], in_ch=64, out_ch=32)
        blk04_hn = _merge_decode_block(blk13_hn, [blk00_hn, blk01_hn, blk02_hn, blk03_hn], in_ch=64, out_ch=32)

        blk01_hn = HiddenNode(prev=[blk01_hn], layers=[Conv2D(num_filters=nclass, kernel_size=(1,1), stride=(1,1), padding='SAME')])
        blk02_hn = HiddenNode(prev=[blk02_hn], layers=[Conv2D(num_filters=nclass, kernel_size=(1,1), stride=(1,1), padding='SAME')])
        blk03_hn = HiddenNode(prev=[blk03_hn], layers=[Conv2D(num_filters=nclass, kernel_size=(1,1), stride=(1,1), padding='SAME')])
        blk04_hn = HiddenNode(prev=[blk04_hn], layers=[Conv2D(num_filters=nclass, kernel_size=(1,1), stride=(1,1), padding='SAME')])

        self.endnode = EndNode(prev=[blk01_hn, blk02_hn, blk03_hn, blk04_hn])
