/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class SQL2MR {

  public static class TokenizerMapper 
       extends Mapper<Object, Text, Text, FloatWritable>{
    
    private Text outputKey = new Text();
    private FloatWritable outputValue = new FloatWritable();
      
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
        
        // transaction_id,transaction_date,transaction_time,transaction_qty,store_id,store_location,product_id,unit_price,product_category,product_type,product_detail
        
        // SELECT store_location, sum(transaction_qty * unit_price)
        // FROM coffee_shop_sales
        // where product_category = 'Coffee'
        // group by store_location
        // having count(*) >= 20000

        String[] toks = value.toString().split(",");
        String store_location = toks[5];
        int transaction_qty = Integer.parseInt(toks[3]);
        double unit_price = Double.parseDouble(toks[7]);
        String product_category = toks[8];

        if ("Coffee".equals(product_category)) {
          float transactionAmount = (float) (transaction_qty * unit_price);
          outputKey.set(store_location);
          outputValue.set(transactionAmount);
          context.write(outputKey, outputValue);
        }
    }
  }
  
  public static class MyReducer 
       extends Reducer<Text,FloatWritable,Text,FloatWritable> {
    private FloatWritable result = new FloatWritable();

    public void reduce(Text key, Iterable<FloatWritable> values, 
                       Context context
                       ) throws IOException, InterruptedException {
    
      float sum = 0;
      int count = 0;

      for (FloatWritable val : values) {
        sum += val.get();
        count++;
      }
      if (count >= 20000) {
        result.set(sum);
        context.write(key, result);

    }
  }
}
  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
    if (otherArgs.length < 2) {
      System.err.println("Usage: sql2mr <in> [<in>...] <out>");
      System.exit(2);
    }
    Job job = Job.getInstance(conf, "sql2mr");
    job.setJarByClass(SQL2MR.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setReducerClass(MyReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(FloatWritable.class);
    for (int i = 0; i < otherArgs.length - 1; ++i) {
      FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
    }
    FileOutputFormat.setOutputPath(job,
      new Path(otherArgs[otherArgs.length - 1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
