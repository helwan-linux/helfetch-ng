# Maintainer: Your Name <your.email@example.com>
pkgname=helfetch-ng
pkgver=0.1.0 # يمكنك تحديث هذا الإصدار بناءً على إصدار المشروع
pkgrel=1
pkgdesc="A system information tool inspired by Neofetch." # وصف للمشروع
arch=('any')
url="https://github.com/helwan-linux/helfetch-ng"
license=('GPL') # أو الترخيص الفعلي للمشروع إذا كان مختلفًا
depends=('python') # يعتمد على بايثون لتشغيله
source=("${pkgname}::git+${url}.git")
sha256sums=('SKIP') # استخدم 'SKIP' إذا كنت لا ترغب في التحقق من التجزئة، أو قم بإنشائها لاحقًا

build() {
  cd "${srcdir}/${pkgname}"
  # لا توجد خطوات بناء محددة لمشروع بايثون بسيط
}

package() {
  cd "${srcdir}/${pkgname}"
  # إنشاء مجلد الوجهة للبرنامج
  mkdir -p "${pkgdir}/usr/bin"
  mkdir -p "${pkgdir}/usr/share/${pkgname}"

  # نسخ ملفات المشروع إلى مجلد share
  cp -r Helfetch-NG/* "${pkgdir}/usr/share/${pkgname}/"

  # إنشاء سكريبت تشغيل في /usr/bin
  # هذا السكريبت سيقوم بتشغيل ملف __main__.py باستخدام بايثون
  cat << EOF > "${pkgdir}/usr/bin/${pkgname}"
#!/bin/bash
python /usr/share/${pkgname}/__main__.py "\$@"
EOF

  # جعل سكريبت التشغيل قابلاً للتنفيذ
  chmod +x "${pkgdir}/usr/bin/${pkgname}"
}
