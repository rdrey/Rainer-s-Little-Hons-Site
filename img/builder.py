import sys, subprocess, re, glob, os, fnmatch

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.md'):
        print file

        md_content_file = file
        html_content_file = md_content_file + ".html"
        output_file_name = md_content_file[0:-3] + ".html"

        write_arg = "+w " + html_content_file
        subprocess.call(["vim", md_content_file, "+TOhtml", write_arg, "+qall!" ])

        vim_html = open(html_content_file)
        vim_html = vim_html.read() # I wonder if there is a one-liner to do this.

        p = re.compile('<pre>.*</pre>' , re.S)
        m = p.search(vim_html)
        vim_html = m.group()

        
        # print nav_tag
        # cur = re.compile(nav_tag)
        # print cur.search(vim_html)
        # vim_html = cur.sub('<p class="current"><a href="'+output_file_name+'">"'+output_file_name+'"</a></p>', vim_html)
        
        img = re.compile('<span class="Special">!\[</span><span class="Underlined">(.*)</span><span class="Special">\]\(</span><span class="Constant">(.*)</span><span class="Special">\)</span>')
        print "images: ", img.findall(vim_html)
        vim_html = img.sub(r'<span class="Special">![</span><span class="Underlined">\1</span><span class="Special">](</span><span class="Constant">\2</span><span class="Special">)</span>\n<img src="\2" alt="\1"/>', vim_html)

        link = re.compile('<span class="Special">\[</span><span class="Underlined">([^<]*)</span><span class="Special">\]\(</span><span class="Constant">([^:~\)]*)</span><span class="Special">\)</span>')
        print "links: ", link.findall(vim_html)
        vim_html = link.sub(r'<span class="Special">[</span><span class="Underlined"><a href="\2">\1</a></span><span class="Special">](</span><span class="Constant">\2</span><span class="Special">)</span>', vim_html)

        people = re.compile('<span class="Special">\[</span><span class="Underlined">(.*)</span><span class="Special">\]\(</span><span class="Constant">(~[^:\)]*)</span><span class="Special">\)</span>')
        print "people: ", people.findall(vim_html)
        vim_html = people.sub(r'<span class="Special">[</span><span class="Underlined"><a href="http://people.cs.uct.ac.za/\2">\1</a></span><span class="Special">](</span><span class="Constant">\2</span><span class="Special">)</span>', vim_html)

        outlink = re.compile('<span class="Special">\[</span><span class="Underlined">(.*)</span><span class="Special">\]\(</span><span class="Constant"><a href="(.*)".*</span><span class="Special">\)</span>')
        print "outlinks: ", outlink.findall(vim_html)
        vim_html = outlink.sub(r'<span class="Special">[</span><span class="Underlined"><a href="\2">\1</a></span><span class="Special">](</span><span class="Constant">\2</span><span class="Special">)</span>', vim_html)


        frame = open("frame.html")
        frame = frame.read()

        output = p.sub(vim_html, frame)

        nav_tag = '<p><a href="'+output_file_name+'">'+output_file_name+'</a></p>'
        output = output.replace(nav_tag, '<p class="current"><a href="'+output_file_name+'">'+output_file_name+'</a></p>')

        output = output.replace('<div id="tab">index.html</div>', '<div id="tab">'+output_file_name+"</div>")

        output_file = open(output_file_name, "w")
        output_file.write(output)
        output_file.close()

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.md.html'):
        os.remove(file)