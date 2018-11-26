import bs4
import requests


def get_html(url):
    """
    웹 사이트 주소를 입력 받아, html tag 를 읽어드려 반환한다.
    :param url: parsing target web url
    :return: html tag
    """
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        return '제품 정보가 없습니다.'
    else:
        return response.text

def get_url(data):
    url_main = data.select('div.productLists div.gridRow div.threeColumn div.image a')
    url = []
    for i in url_main:
        url.append("https://www.ikea.com/" + i.get('href'))
    return url

class parsing_data:
    def __init__(self, in_url):
        self.html= get_html(in_url)
        self.data = bs4.BeautifulSoup(self.html, 'html.parser')
        self.image = []
        self.name = []
        self.price = []
        self.size = []
        self.url = get_url(self.data)

    def get_img(self, sub):
        sub_main = sub.select('div.rightContent div.pipContainer div#leftMainContainer div.rightContentContainer img#productImg')
        sub_main = str(sub_main[0]).split(' ')
        for line in sub_main:
            if 'src' in line:
                line = line.replace('"', '')
                line = line.replace('src=', '')
                self.image.append(line)
        return self.image

    def get_name(self, sub):
        name_now = sub.select('div.addList div.rightInfoDiv h1 span.productName')
        for i in name_now:
            name_in = i.getText().strip()
            self.name.append(name_in)
        return self.name

    def get_price(self, sub):
        price_now = sub.select('div.addList div.rightInfoDiv div.priceContainer span.packagePrice')
        for i in price_now:
            price_in = i.getText().strip()
            price_in = str(price_in).replace('\xa0', '')
            self.price.append(price_in)
        return self.price

    def get_size(self, sub):
        size_now = sub.select('div#metric')
        for i in size_now:
            size_in = i.getText().strip()
            size_in = str(size_in).split(' cm')
            print(size_in)
            if len(size_in) < 3:
                self.size.append('none size')
            else:
                self.size.append([size_in[0].split(': ')[1],size_in[1].split(': ')[1],size_in[2].split(': ')[1]])
        return self.size

    def print_all(self):
        for i in self.url:
            sub_html = get_html(i)
            if sub_html == '제품 정보가 없습니다.':
                pass
            else:
                sub = bs4.BeautifulSoup(sub_html, 'html.parser')
                self.get_name(sub)
                self.get_price(sub)
                self.get_size(sub)
                self.get_img(sub)
        return self.url, self.name, self.price, self.image, self.size

class chair(parsing_data):
    def get_size(self,sub):
        size_now = sub.select('div#metric')
        for i in size_now:
            size_in = i.getText().strip()
            size_in = str(size_in).split(' cm')
            print(size_in)
            if len(size_in) < 2:
                self.size.append('none size')
            else:
                if '시험 중량: ' in size_in[0]:
                    self.size.append([size_in[0].split(': ')[2], size_in[1].split(': ')[1], size_in[2].split(': ')[1]])
                else:
                    self.size.append([size_in[0].split(': ')[1], size_in[1].split(': ')[1], size_in[2].split(': ')[1]])
        return self.size

class table(parsing_data):
    def get_size(self, sub):
        size_now = sub.select('div#metric')
        for i in size_now:
            size_in = i.getText().strip()
            size_in = str(size_in).split(' cm')
            print(size_in)
            if len(size_in)<2:
                self.size.append('none size')
            elif len(size_in) == 3:
                self.size.append([size_in[0].split(': ')[1], size_in[1].split(': ')[1]])
            elif len(size_in) > 3:
                self.size.append([size_in[0].split(': ')[1], size_in[1].split(': ')[1], size_in[2].split(': ')[1]])
        return self.size


#class 처리
#소파
'''SOFA = parsing_data('https://www.ikea.com/kr/ko/catalog/categories/departments/living_room/39130/')
url, name, price, image, size = SOFA.print_all()
print(len(url), url)
print(len(name), name)
print(len(price), price)
print(len(image), image)
print(len(size), size)'''

#의자
'''CHAIR = chair('https://www.ikea.com/kr/ko/catalog/categories/departments/dining/25219/')
url, name, price, image, size = CHAIR.print_all()
print(len(url), url)
print(len(name), name)
print(len(price), price)
print(len(image), image)
print(len(size), size)'''

#책상
'''TABLE = table('https://www.ikea.com/kr/ko/catalog/categories/departments/dining/21825/')
url, name, price, image, size = TABLE.print_all()
print(len(url), url)
print(len(name), name)
print(len(price), price)
print(len(image), image)
print(len(size), size)'''

#옷장
'''CLOS = parsing_data('https://www.ikea.com/kr/ko/catalog/categories/departments/bedroom/10451/')
url, name, price, image, size = CLOS.print_all()
print(len(url), url)
print(len(name), name)
print(len(price), price)
print(len(image), image)
print(len(size), size)'''