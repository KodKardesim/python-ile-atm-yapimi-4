from os import system
import smtplib
from email.message import EmailMessage
from random import randint

msg = EmailMessage()


mail_adresi = "e-mail adresin"  # Kendi mail adresiniz
sifre = "sifreniz"  # Şifreniz

mail = smtplib.SMTP("smtp.gmail.com", 587)  # Gmail sunucusuna bağlantı tanımladık.
mail.starttls()  # Bağlantıyı başlattık.

mail.login(mail_adresi, sifre)  # Giriş yaptık.

def MailGonder(alici, konu, metin): # Yeni bir mail gönderim metodu kullandık
		msg["Subject"] = konu
		msg["From"] = "Kod Kardeşim"
		msg["To"] = alici
		msg.set_content(metin)
		mail.send_message(msg)
		del msg['Subject']
		del msg['From']
		del msg['To']

class Musteri:
		def __init__(self, ID, PAROLA, ISIM, EMAIL):
				self.id = ID
				self.parola = PAROLA
				self.isim = ISIM
				self.email = EMAIL
				self.bakiye = 0


class Banka:
		def __init__(self):
				self.musteriler = list()

		def MusteriOl(self, ID, PAROLA, ISIM, EMAIL):
				self.musteriler.append(Musteri(ID, PAROLA, ISIM, EMAIL))


banka = Banka()
uyeislem = """
[1] Bakiye sor
[2] Para yatır
[3] Para gönder
[4] Para çek
[Q] Çıkış yap"""
while True:
	system("cls")
	idler = [i.id for i in banka.musteriler]
	print("""[1] Banka Müşterisiyim
[2] Banka Müşterisi olmak istiyorum""")
	secim = input("Seçiminiz : ")
	if secim == "1":
		gelenid = input("ID GİRİNİZ : ")
		gelenparola = input("Parola giriniz: ")
		if gelenid in idler:
			for musteri in banka.musteriler:
				if gelenid == musteri.id:  # musteri bulundu

					if gelenparola == musteri.parola:
						print("Giriş Başarılı.")
						MailGonder(musteri.email, "Bir cihaz hesabınıza giriş yaptı", f"Sevgili {musteri.isim}, az önce hesabınıza giriş yapıldı. Bu siz değilseniz şifrenizi değiştirerek hesabınızı güvende tutabilirsiniz")
						while True:
							system("cls")
							print("Hoşgeldiniz {}".format(musteri.isim))
							print(uyeislem)
							islem = input("İşlem seçiniz : ")
							if islem == "1":
								print(f"Mevcut bakiyeniz : {musteri.bakiye} TL")
								input("Ana menüye ddönmek için 'enter'a basınız.")
							elif islem == "2":
								try:
									miktar = int(input("Yatırmak istediğiniz miktar : "))
									onay = input(f"Hesabınıza {miktar} TL yatırma işlemini onaylıyor musunuz. [E/e]")
									if onay == "E" or onay == "e":
										musteri.bakiye += miktar
										print(f"Hesabınıza {miktar} TL yatırıldı.")
										MailGonder(musteri.email,"Hesabınıza para yatırıldı",f"Sevgili {musteri.isim}, az önce hesabınıza {miktar} TL yatırıldı.")
										input("Ana menüye dönmek için 'enter'a basınız.")
									else:
										print("İşlem iptal edildi.")
										input("Ana menüye dönmek için 'enter'a basınız.")
								except:
									print("Lütfen 'rakam' kullanarak miktar girin.")
									input("Ana menüye dönmek için 'enter'a basınız.")
							elif islem == "3":
								arananID = input("Müşteri ID : ")
								if arananID in idler:
									for digermusteri in banka.musteriler:
										if arananID == digermusteri.id:
											print(f"Para gönderme işlemi : {digermusteri.isim} ")
											try:
												miktar = int(input("Göndermek istediğiniz miktar :"))
												if miktar <= musteri.bakiye:
													onay = input(
														f"{digermusteri.isim} adlı kişinin hesabına {miktar} TL yatırma işlemini onaylıyor musunuz. [E/e]")
													if onay == "E" or onay == "e":
														digermusteri.bakiye += miktar
														musteri.bakiye -= miktar
														print(f"{digermusteri.isim}'a {miktar} TL yatırıldı.")
														MailGonder(musteri.email,"Para gönderme işlemi",f"Sevgili {musteri.isim}, hesabından {digermusteri.isim} adlı kişinin hesabına {miktar} TL gönderildi.")
														MailGonder(digermusteri.email,"Hesabına para geldi", f"Sevgili {digermusteri.isim} hesabına {musteri.isim} tarafından {miktar} TL gönderildi.")
														input("Ana menüye dönmek için 'enter'a basınız.")
													else:
														print("İşlem iptal edildi.")
														input("Ana menüye dönmek için 'enter'a basınız.")
												else:
													print("Yetersiz bakiye")
													input("Ana menüye dönmek için 'enter'a basınız.")
											except:
												print("Lütfen 'rakam' kullanarak miktar girin.")
												input("Ana menüye dönmek için 'enter'a basınız.")
								else:
									print("Müşteri bulunamadı.")
									input("Ana menüye dönmek için 'enter'a basınız.")
							elif islem == "4":
								print("Para Çekme İşlemi")
								try:
									miktar = int(input("Çekmek istediğiniz miktar : "))
									if miktar <= musteri.bakiye:
										onay = input(
											f"Hesabınızdan {miktar} TL çekme işlemini onaylıyor musunuz. [E/e]")
										if onay == "E" or onay == "e":
											musteri.bakiye -= miktar
											print(f"Hesabınızdan {miktar} TL çekildi.")
											MailGonder(musteri.email,"Hesabınızdan para çekildi.",f"Sevgili {musteri.isim}, az önce hesabınızdan {miktar} TL çekildi.")
											input("Ana menüye dönmek için 'enter'a basınız.")
										else:
											print("İşlem iptal edildi.")
											input("Ana menüye dönmek için 'enter'a basınız.")
									else:
										print("Yetersiz bakiye")
										input("Ana menüye dönmek için 'enter'a basınız.")
								except:
									print("Lütfen 'rakam' kullanarak miktar girin.")
									input("Ana menüye dönmek için 'enter'a basınız.")
							elif islem == "Q" or islem == "q":
								print("Çıkış yapıldı")
								break
					else:
						print("Parola hatalı.")
						islem = input("Şifrenizi sıfırlamak ister misiniz? EVET : [E/e] -- Hayır : [H/h]")
						if islem == "E" or islem == "e":
							guvenlikkodu = randint(10000000,999999999)
							MailGonder(musteri.email, "Şifre sıfırlama kodu", f"Sevgili {musteri.isim} şifrenizi değiştirmek için bu kodu kullanabilirsiniz : {guvenlikkodu}")
							print("Email hesabınıza bir güvenlik kodu gönderildi. Kodu girerek şifrenizi değiştirebilirsiniz")
							gelenguvenlikkodu = input("Güvenlik kodu : ")
							if str(guvenlikkodu) == gelenguvenlikkodu:
								yeniparola = input("Yeni parolanızı giriniz")
								musteri.parola = yeniparola 
								print("Başarılı! Parolanız değiştirildi.")
								input("Ana menüye dönmek için 'enter'a basınız.")
							else:
								print("Güvenlik kodu yanlış!")
								input("Ana menüye dönmek için 'enter'a basınız.")
						else:
							input("Ana menüye dönmek için 'enter'a basınız.")
							break
		else:
			print("ID veya Parola hatalı.")
			input("Ana menüye dönmek için 'enter'a basınız.")

	if secim == "2":
		print("Kayıt Formu")
		isim = input("İsminiz : ")
		ID = input("ID belirleyiniz: ")
		if ID in idler:
			print("Bu ID alınmış :( Lütfen başka bir ID dene.")
			input("Ana menüye dönmek için 'enter'a basınız.")
		else:
			parola = input("Parola belirleyiniz : ")
			email = input("Email adresi : ")
			banka.MusteriOl(ID, parola, isim, email)
			print("Bankamıza üye olduğunuz için teşekkür ederiz.")
			MailGonder(email,"Bankamıza Hoşgeldiniz", "Kod Kardeşim banka müşterisi olduğunuz için teşekkür ederiz:)")
			input("Ana menüye dönmek için 'enter'a basınız.")
