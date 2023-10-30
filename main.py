import os
import threading
import requests
from bs4 import BeautifulSoup
import re
import customtkinter as ctk
from customtkinter import INSERT

def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


def main():
    top=ctk.CTk()
    top.geometry('450x500')
    top.title('360小说下载')
    top.resizable(height=False, width=False)
    check=ctk.CTkCheckBox(top,text='合并',width=60)
    check.grid(row=0,column=1)

    #网址输入框
    input=ctk.CTkEntry(top,width=200,)
    input.insert('1','这里输入主页面网址...')
    input.grid(row=0,column=0,padx=5,pady=10)
    #下载按钮

    def call_down():
        if input.get():
            # print(type(input.get()))
            # try:
            down_load(input.get())
            # except:
            #     pass
                # messagebox.showwarning('错误','网址格式错误！')
        else:
            pass
            # messagebox.showwarning('错误','未输入网址！')
    down_btn=ctk.CTkButton(
        top,width=50,
        text='下载',
        command=lambda : thread_it(call_down)
    )
    down_btn.grid(row=0,column=2,padx=5,pady=10)
    #清空按钮
    def call_clear():
        input.delete('0','end')
    clear_btn=ctk.CTkButton(
        top,
        text='清空',width=50,
        command=call_clear
    )
    clear_btn.grid(row=0,column=3,padx=5,pady=10)
    # 进度显示框
    txtbox = ctk.CTkTextbox(
        top,
        width=380,
        height=400,
        undo=True,
        autoseparators=False,
        wrap='word',
    )
    txtbox.insert(INSERT, '')
    txtbox.grid(row=1,column=0,columnspan=4,padx=5,pady=10)
    def down_load(url):
        # global txtbox

        txtbox.delete('1.0','end')
        obj=re.compile("book(?P<key>.*?)360xs",re.S)
        obj2=re.compile("eval(?P<fun>.*?)eval",re.S)
        head={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
            ,'cookie': 'PHPSESSID=svelp4ffl0e8b5gejim9ip11e1; rc=1; mlight=0; sid=Q4ESDGcF4RtXFXohVNYAcpaYTjbpzIs6; uid=177232; rcapter=149443=82848070&140475=74213530'
        }
        resp=requests.get(url,headers=head)
        page=BeautifulSoup(resp.text)
        h1=page.find('h1')
        a=h1.find_all('a')[0]
        dir_name=a.text
        txtbox.insert('end', '获取小说 ' + dir_name + ' 成功！\n')
        txtbox.update()
        try:
            os.makedirs(f'./{dir_name}')
        except:
            pass
        # div_list=page.find_all('div' ,class_="dc-cap")
        div_page=page.find("div",class_="pageselect")
        option=div_page.find_all("option")
        print(option)
        for op in option:
            src="https://m.e360xs.com"+op["value"]
            resp = requests.get(src, headers=head)
            page = BeautifulSoup(resp.text)
            # h1 = page.find('h1')
            # a = h1.find_all('a')[0]
            # dir_name = a.text
            div_list = page.find_all('div', class_="dc-cap")
            count=0
            if not check.get():
                for div in div_list:
                    count+=1
                    if count<=0:
                        continue
                    else:
                        a=div.find('a')
                        href='https://m.360xs.com'+a['href']
                        name=a.text
                        # print(name,href)
                        main_href = href.split('/')
                        main_href.pop(-1)
                        main_href = '/'.join(main_href)
                        name=name.replace(" ","").replace("？","").replace("\n","").replace("\r","").replace(">","").replace("<","").replace("\\","").replace("*","").replace("/","").replace("?","")
                        f=open(f'./{dir_name}/{name}.txt','w',encoding='utf-8')
                        while True:
                            resp2=requests.get(href,headers=head)
                            # print('访问',href)
                            page2=BeautifulSoup(resp2.text)
                            script_list=obj2.finditer(resp2.text)
                            # print(resp2.text)
                            for scri in script_list:
                                txt=scri.group("fun")
                                # print(txt)
                                # break
                            key=obj.finditer(txt)
                            for k in key:
                                next_key=k.group('key').split('|')[1]
                            # print(next_key)
                            # print(main_href)
                            next_url=main_href+'/'+next_key+'.html'
                            href=next_url
                            # print(next_url)
                            div=page2.find('div',class_='chapter')
                            p_list=div.find_all('p')
                            content=''
                            for p in p_list:
                                # content+='\t'
                                content+=p.text
                                content+='\n'
                            content=content.replace('（本章节未完结，点击下一页翻页继续阅读）','')
                            # print(content)
                            f.write(content)
                            if '下一章' in resp2.text:
                                break
                        print(name,'下载完成！')
                        txtbox.insert('end',name+'下载完成！\n')
                        txtbox.update()
                        f.close()
            else:
                f = open(f'./{dir_name}/{dir_name}.txt', 'w', encoding='utf-8')
                for div in div_list:
                    count+=1
                    if count<=0:
                        continue
                    else:
                        a=div.find('a')
                        href='https://m.360xs.com'+a['href']
                        name=a.text
                        f.write(name+'\n')
                        # print(name,href)
                        main_href = href.split('/')
                        main_href.pop(-1)
                        main_href = '/'.join(main_href)
                        name=name.replace(" ","").replace("？","").replace("\n","").replace("\r","").replace(">","").replace("<","").replace("\\","").replace("*","").replace("/","").replace("?","")
                        while True:
                            resp2=requests.get(href,headers=head)
                            # print('访问',href)
                            page2=BeautifulSoup(resp2.text)
                            script_list=obj2.finditer(resp2.text)
                            # print(resp2.text)
                            for scri in script_list:
                                txt=scri.group("fun")
                                # print(txt)
                                # break
                            key=obj.finditer(txt)
                            for k in key:
                                next_key=k.group('key').split('|')[1]
                            # print(next_key)
                            # print(main_href)
                            next_url=main_href+'/'+next_key+'.html'
                            href=next_url
                            # print(next_url)
                            div=page2.find('div',class_='chapter')
                            p_list=div.find_all('p')
                            content=''
                            for p in p_list:
                                # content+='\t'
                                content+=p.text
                                content+='\n'
                            content=content.replace('（本章节未完结，点击下一页翻页继续阅读）','')
                            # print(content)
                            f.write(content)
                            if '下一章' in resp2.text:
                                break
                        print(name,'下载完成！')
                        txtbox.insert('end',name+'下载完成！\n')
                        txtbox.update()
                f.close()
        txtbox.insert('end', '全部下载完成！\n')
        txtbox.update()
    top.mainloop()
if __name__ == '__main__':
    main()
