#fast php template

python script  generate simple php template

最快的php模板系统就是php html混合本身，对于小型网站（page number <20)的网站，用混合模式生成页面效率最高

模板语法借鉴于jinjia，采用 `{{  }}` 和`{%  %}` 作为隔离符号

##支持语法

- 变量：{{ var }} {{ var.attr }} {{ var.0 }}
- 遍历
		
		{% for x in xxx %} 
			//do something .... 
		{% endfor;%}

- 条件判断

		{% if xxx %} 
			//do something .... 
		{% endif;%}

- filter 函数支持
	`{{  var|strtolower }}`

##例子

- 编写一个简单的php模板，如下

		<html>
		<body>
		{% for item in obj_list %}
		<a href="{{ item.url }}" id="id-{{ loop.index }}">{{ item.title }}<span>{{ item.tags.0 }}</span></a>
		{% endfor;%}
		</body>
		</html>

- 执行 <code>fmt.py test.php </code> 得到如下结果  
		
		<html>
		<body>
		<?php foreach($obj_list as $loop_index =>&$item): ?>
		<a href="<?php echo $item['url'];?>" id="id-<?php echo ($loop_index+1);?>"><?php echo $item['title'];?><span><?php echo $item['tags'][0];?></span></a>
		<?php endforeach;?>
		</body>
		</html>

##提示
- fmt.py 生成器是可以重入的，可以对php文件反复执行，不会破坏结构
- [Document(english)](http://code.google.com/p/fast-php-template/)