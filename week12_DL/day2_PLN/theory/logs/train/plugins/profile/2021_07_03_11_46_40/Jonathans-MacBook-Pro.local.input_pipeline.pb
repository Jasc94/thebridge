	???x??J@???x??J@!???x??J@	???j?????j??!???j??"{
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails:???x??J@?A`??"??A5^?I?J@Y)\???(??rEagerKernelExecute 0*	      [@2F
Iterator::ModelD?l?????!?q??O@)D?l?????1?q??O@:Preprocessing2g
0Iterator::Model::MaxIntraOpParallelism::Prefetch?I+???!?%???^4@)?I+???1?%???^4@:Preprocessing2t
=Iterator::Model::MaxIntraOpParallelism::Prefetch::MemoryCache?? ?rh??!???^B{/@)?~j?t???1??8??8&@:Preprocessing2x
AIterator::Model::MaxIntraOpParallelism::Prefetch::MemoryCacheImpl{?G?zt?!Lh/???@){?G?zt?1Lh/???@:Preprocessing:?
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
?Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
?Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
?Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
?Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)?
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis?
device?Your program is NOT input-bound because only 0.2% of the total step time sampled is waiting for input. Therefore, you should focus on reducing other time.no*no9???j??I?.????X@Zno#You may skip the rest of this page.B?
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown?
	?A`??"???A`??"??!?A`??"??      ??!       "      ??!       *      ??!       2	5^?I?J@5^?I?J@!5^?I?J@:      ??!       B      ??!       J	)\???(??)\???(??!)\???(??R      ??!       Z	)\???(??)\???(??!)\???(??b      ??!       JCPU_ONLYY???j??b q?.????X@