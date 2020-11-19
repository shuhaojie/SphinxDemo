
from ...node import StartNode, HiddenNode, EndNode
from ...layers import BaseModel, Conv2D, RELU, MaxPooling, Concat, BatchNormalization, \
                      ImageResize, Sum, Multiply
from ...utils import valid_nd

class R2UNet(BaseModel):

    @BaseModel.init_name_scope
    def __init__(self, input_shape, nclass, t, attention=False):
        '''
        define a R2UNet model object.
        Paper: https://arxiv.org/abs/1802.06955

        Args:
            input_shape (tuple): (h, w)
            nclass (int): The number of classes of the ouput mask.
            t (int): Recurrent time step
            attention (bool): To include attention block
        '''

        def _recurrent_block(in_hn, out_ch, t):
            blk = []
            blk.append(Conv2D(num_filters=out_ch, kernel_size=(3,3), stride=(1,1), padding='SAME'))
            blk.append(BatchNormalization())
            blk.append(RELU())

            out_hn = HiddenNode(prev=[in_hn], layers=blk)

            for _ in range(t-1):
                out_hn = HiddenNode(prev=[in_hn, out_hn], input_merge_mode=Sum(), layers=blk)

            return out_hn

        def _rrcnn_block(in_hn, out_ch, t):
            blk = []
            blk.append(Conv2D(num_filters=out_ch, kernel_size=(1,1), stride=(1,1), padding='SAME'))

            out_hn = HiddenNode(prev=[in_hn], layers=blk)

            res_hn = _recurrent_block(out_hn, out_ch, t)
            res_hn = _recurrent_block(res_hn, out_ch, t)

            out_hn = HiddenNode(prev=[out_hn, res_hn], input_merge_mode=Sum(), layers=[])

            return out_hn

        def _attention_block(x_hn, g_hn, out_ch):
            blk_g = []
            blk_g.append(Conv2D(num_filters=out_ch, kernel_size=(1,1), stride=(1,1), padding='SAME'))
            blk_g.append(BatchNormalization())

            blk_x = []
            blk_x.append(Conv2D(num_filters=out_ch, kernel_size=(1,1), stride=(1,1), padding='SAME'))
            blk_x.append(BatchNormalization())

            blk_psi = []
            blk_psi.append(RELU())
            blk_psi.append(Conv2D(num_filters=1, kernel_size=(1,1), stride=(1,1), padding='SAME'))
            blk_psi.append(BatchNormalization())
            blk_psi.append(Sigmoid())

            g1_hn = HiddenNode(prev=[g_hn], layers=blk_g)
            x1_hn = HiddenNode(prev=[x_hn], layers=blk_x)
            psi_hn = HiddenNode(prev=[g1_hn, x1_hn], input_merge_mode=Sum(), layers=blk_psi)

            out_hn = HiddenNode(prev=[psi_hn, x_hn], input_merge_mode=Multiply(), layers=[])

            return out_hn

        def _downsample(in_hn, shape):
            out_hn = HiddenNode(prev=[in_hn], layers=[MaxPooling(poolsize=(2,2), stride=(2,2), padding='VALID')])
            shape = valid_nd(shape, kernel_size=(2,2), stride=(2,2))

            return out_hn, shape

        def _upsample(in_hn, out_shape, out_ch):
            blk = []
            blk.append(ImageResize(out_shape))
            blk.append(Conv2D(num_filters=out_ch, kernel_size=(3,3), stride=(1,1), padding='SAME'))
            blk.append(BatchNormalization())
            blk.append(RELU())

            out_hn = HiddenNode(prev=[in_hn], layers=blk)

            return out_hn

        # encoding
        self.startnode= StartNode(input_vars=[None])
        eblk1_hn = _rrcnn_block(self.startnode, 64, t)

        eblk2_hn, shape2 = _downsample(eblk1_hn, input_shape)
        eblk2_hn = _rrcnn_block(eblk2_hn, 128, t)

        eblk3_hn, shape3 = _downsample(eblk2_hn, shape2)
        eblk3_hn = _rrcnn_block(eblk3_hn, 256, t)

        eblk4_hn, shape4 = _downsample(eblk3_hn, shape3)
        eblk4_hn = _rrcnn_block(eblk4_hn, 512, t)

        eblk5_hn, shape5 = _downsample(eblk4_hn, shape4)
        eblk5_hn = _rrcnn_block(eblk5_hn, 1024, t)

        # downsampling + conv
        dblk5_hn = _upsample(eblk5_hn, shape4, 512)
        if attention: eblk4_hn = _attention_block(eblk4_hn, dblk5_hn, 256)
        dblk5_hn = HiddenNode(prev=[eblk4_hn, dblk5_hn], input_merge_mode=Concat(axis=-1), layers=[])
        dblk5_hn = _rrcnn_block(dblk5_hn, 512, t)

        dblk4_hn = _upsample(dblk5_hn, shape3, 256)
        if attention: eblk3_hn = _attention_block(eblk3_hn, dblk4_hn, 128)
        dblk4_hn = HiddenNode(prev=[eblk3_hn, dblk4_hn], input_merge_mode=Concat(axis=-1), layers=[])
        dblk4_hn = _rrcnn_block(dblk4_hn, 256, t)

        dblk3_hn = _upsample(dblk4_hn, shape2, 128)
        if attention: eblk2_hn = _attention_block(eblk2_hn, dblk3_hn, 64)
        dblk3_hn = HiddenNode(prev=[eblk2_hn, dblk3_hn], input_merge_mode=Concat(axis=-1), layers=[])
        dblk3_hn = _rrcnn_block(dblk3_hn, 128, t)

        dblk2_hn = _upsample(dblk3_hn, input_shape, 64)
        if attention: eblk1_hn = _attention_block(eblk1_hn, dblk2_hn, 32)
        dblk2_hn = HiddenNode(prev=[eblk1_hn, dblk2_hn], input_merge_mode=Concat(axis=-1), layers=[])
        dblk2_hn = _rrcnn_block(dblk2_hn, 64, t)

        dblk1_hn = HiddenNode(prev=[dblk2_hn], layers=[Conv2D(nclass, kernel_size=(1,1), stride=(1,1), padding='SAME')])

        self.endnode = EndNode(prev=[dblk1_hn])
