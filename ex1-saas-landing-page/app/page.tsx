"use client";

import { useState } from "react";
import Image from "next/image";
import {
  Sparkles,
  CheckCircle2,
  SlidersHorizontal,
  Globe2,
  FileText,
  Users,
  ChevronRight,
  PlayCircle,
  Plus,
  Rocket
} from "lucide-react";

export default function Home() {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">W</span>
            </div>
            <span className="font-bold text-xl tracking-tight">WriteFlow</span>
          </div>

          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
            <a href="#features" className="hover:text-indigo-600 transition-colors">기능 소개</a>
            <a href="#pricing" className="hover:text-indigo-600 transition-colors">요금제</a>
            <a href="#faq" className="hover:text-indigo-600 transition-colors">FAQ</a>
          </div>

          <div className="flex items-center gap-3">
            <button className="hidden sm:block px-4 py-2 text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-full transition-colors">
              로그인
            </button>
            <button className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-full transition-colors">
              무료 체험 시작
            </button>
          </div>
        </div>
      </nav>

      <main>
        {/* Hero Section */}
        <section className="pt-32 pb-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-[#4F25C8] to-[#6D28D9] text-white text-center">
          <div className="max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 border border-white/20 text-sm font-medium mb-8 backdrop-blur-sm">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
              v2.0 업데이트 출시
            </div>

            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8 leading-tight">
              AI와 함께<br />더 빠르게 더 잘 쓰세요
            </h1>

            <p className="text-lg md:text-xl text-indigo-100 mb-10 max-w-2xl mx-auto leading-relaxed">
              아이디어를 몇 초 만에 완성된 콘텐츠로 바꿔보세요.<br className="hidden md:block" />
              블로그, 이메일, 소셜 미디어 게시물까지, WriteFlow가 도와드립니다.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <button className="w-full sm:w-auto px-8 py-3.5 bg-white text-indigo-600 rounded-full font-semibold flex items-center justify-center gap-2 hover:bg-indigo-50 transition-colors shadow-lg">
                무료 체험 시작
                <ChevronRight className="w-4 h-4" />
              </button>
              <button className="w-full sm:w-auto px-8 py-3.5 bg-indigo-800/50 text-white rounded-full font-semibold flex items-center justify-center gap-2 hover:bg-indigo-800 transition-colors backdrop-blur-sm border border-indigo-700">
                <PlayCircle className="w-5 h-5" />
                데모 보기
              </button>
            </div>

            <p className="mt-6 text-sm text-indigo-200">
              신용카드 필요 없음 · 14일 무료 체험 · 언제든 취소 가능
            </p>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <span className="text-indigo-600 font-semibold mb-2 block">주요 기능</span>
              <h2 className="text-3xl md:text-4xl font-bold mb-4">당신의 글쓰기를 완벽하게 지원합니다</h2>
              <p className="text-slate-600 max-w-2xl mx-auto text-lg">
                WriteFlow의 강력한 AI 엔진이 초안 작성부터 교정까지,<br className="hidden sm:block" />창작의 모든 과정을 함께합니다.
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Feature 1 */}
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center mb-6">
                  <Sparkles className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-3">AI 작문 보조</h3>
                <p className="text-slate-600 leading-relaxed">
                  간단한 키워드만 입력하면 AI가 문맥을 파악하여 자연스러운 초안을 순식간에 작성해줍니다.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center mb-6">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-3">완벽한 문법 교정</h3>
                <p className="text-slate-600 leading-relaxed">
                  복잡한 문법 규칙과 맞춤법 오류를 실시간으로 감지하고 교정하여 전문성을 높여줍니다.
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center mb-6">
                  <SlidersHorizontal className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-3">톤 앤 매너 조정</h3>
                <p className="text-slate-600 leading-relaxed">
                  '전문적인', '친근한', '설득력 있는' 등 원하는 어조를 선택하여 글의 분위기를 바꿀 수 있습니다.
                </p>
              </div>

              {/* Feature 4 */}
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-pink-50 text-pink-600 rounded-xl flex items-center justify-center mb-6">
                  <Globe2 className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-3">50개국어 지원</h3>
                <p className="text-slate-600 leading-relaxed">
                  전 세계 독자를 위해 50개 이상의 언어로 번역 및 작성이 가능하여 글로벌 진출을 돕습니다.
                </p>
              </div>

              {/* Feature 5 */}
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-orange-50 text-orange-600 rounded-xl flex items-center justify-center mb-6">
                  <FileText className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-3">100+ 템플릿</h3>
                <p className="text-slate-600 leading-relaxed">
                  블로그, 이메일, 광고 카피, SNS 등 다양한 상황에 최적화된 전문 템플릿을 제공합니다.
                </p>
              </div>

              {/* Feature 6 */}
              <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                <div className="w-12 h-12 bg-teal-50 text-teal-600 rounded-xl flex items-center justify-center mb-6">
                  <Users className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold mb-3">실시간 협업</h3>
                <p className="text-slate-600 leading-relaxed">
                  팀원들을 초대하여 문서를 함께 편집하고 실시간으로 피드백을 주고받을 수 있습니다.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing Section */}
        <section id="pricing" className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">합리적인 요금제</h2>
              <p className="text-slate-600 max-w-xl mx-auto mb-8">
                개인 작가부터 대규모 팀까지, <br />
                모든 니즈를 충족하는 플랜을 준비했습니다.
              </p>

              <div className="flex items-center justify-center gap-3">
                <span className={`text-sm font-medium ${!isYearly ? 'text-slate-900' : 'text-slate-500'}`}>월간 결제</span>
                <button
                  onClick={() => setIsYearly(!isYearly)}
                  className="relative inline-flex h-6 w-11 items-center rounded-full bg-indigo-600 transition-colors focus:outline-none"
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition duration-200 ease-in-out ${isYearly ? 'translate-x-6' : 'translate-x-1'}`} />
                </button>
                <span className={`text-sm font-medium ${isYearly ? 'text-slate-900' : 'text-slate-500'}`}>
                  연간 결제 <span className="text-indigo-600 ml-1">(20% 할인)</span>
                </span>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto items-center">
              {/* Free Plan */}
              <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm">
                <h3 className="text-xl font-bold mb-2">Free</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold">$0</span>
                  <span className="text-slate-500">/월</span>
                </div>
                <p className="text-slate-600 mb-8 h-12">가볍게 시작하는 개인 작가를 위한 플랜</p>
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>월 5,000 단어 생성</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>기본 문법 교정</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>10개 템플릿 제공</span></li>
                  <li className="flex items-center gap-3 text-slate-400"><CheckCircle2 className="w-5 h-5" /> <span>톤 앤 매너 조정</span></li>
                </ul>
                <button className="w-full py-3 rounded-xl border border-slate-200 font-semibold hover:bg-slate-50 transition-colors">
                  현재 플랜 사용
                </button>
              </div>

              {/* Pro Plan */}
              <div className="bg-white p-8 rounded-3xl border-2 border-indigo-600 shadow-xl relative transform md:-translate-y-4">
                <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-indigo-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                  가장 인기
                </div>
                <h3 className="text-xl font-bold mb-2">Pro</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold">${isYearly ? '15' : '19'}</span>
                  <span className="text-slate-500">/월</span>
                </div>
                <p className="text-slate-600 mb-8 h-12">전문적인 콘텐츠 제작을 위한 최적의 선택</p>
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span className="font-medium text-slate-900">무제한 단어 생성</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>고급 문법 및 스타일 교정</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>모든 템플릿 및 언어 지원</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>표절 검사 기능</span></li>
                </ul>
                <button className="w-full py-3 rounded-xl bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition-colors shadow-md">
                  무료 체험 시작하기
                </button>
              </div>

              {/* Enterprise Plan */}
              <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm">
                <h3 className="text-xl font-bold mb-2">Enterprise</h3>
                <div className="mb-6">
                  <span className="text-4xl font-bold">${isYearly ? '39' : '49'}</span>
                  <span className="text-slate-500">/월</span>
                </div>
                <p className="text-slate-600 mb-8 h-12">팀 협업과 관리가 필요한 조직을 위한 플랜</p>
                <ul className="space-y-4 mb-8">
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>Pro의 모든 기능 포함</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>최대 5명 팀원 초대</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>공유 워크스페이스</span></li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-5 h-5 text-indigo-600" /> <span>우선 고객 지원</span></li>
                </ul>
                <button className="w-full py-3 rounded-xl border border-slate-200 font-semibold hover:bg-slate-50 transition-colors">
                  영업팀 문의
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section id="faq" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">자주 묻는 질문</h2>

            <div className="space-y-4">
              {[
                { q: "무료 체험 기간은 얼마나 되나요?", a: "가입 후 14일 동안 Pro 플랜의 모든 기능을 무료로 체험하실 수 있습니다." },
                { q: "언제든지 구독을 취소할 수 있나요?", a: "네, 언제든지 마이페이지에서 클릭 한 번으로 구독을 해지하실 수 있습니다. 위약금은 없습니다." },
                { q: "내 데이터는 안전한가요?", a: "모든 데이터는 가장 높은 수준의 보안 프로토콜로 암호화되며, AI 학습에 절대 사용되지 않습니다." },
                { q: "환불 정책은 어떻게 되나요?", a: "결제 후 7일 이내 사용량이 거의 없는 경우 전액 환불해 드립니다." },
                { q: "어떤 결제 수단을 지원하나요?", a: "모든 주요 신용카드와 카카오페이, 네이버페이를 지원합니다." }
              ].map((faq, idx) => (
                <details key={idx} className="group bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden closed">
                  <summary className="flex items-center justify-between p-6 font-semibold cursor-pointer list-none">
                    {faq.q}
                    <span className="transition group-open:rotate-45">
                      <Plus className="w-5 h-5 text-slate-400" />
                    </span>
                  </summary>
                  <div className="px-6 pb-6 text-slate-600 leading-relaxed border-t border-slate-100 pt-4">
                    {faq.a}
                  </div>
                </details>
              ))}
            </div>
          </div>
        </section>

        {/* Bottom CTA Section */}
        <section className="py-24 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-indigo-600 to-violet-600 text-white text-center">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-4xl font-bold mb-6">글쓰기를 혁신할 준비가 되셨나요?</h2>
            <p className="text-xl text-indigo-100 mb-10">
              10,000명 이상의 작가와 마케터들이 WriteFlow와 함께<br /> 더 나은 콘텐츠를 더 빠르게 만들고 있습니다.
            </p>
            <button className="px-8 py-4 bg-white text-indigo-600 rounded-full font-bold text-lg flex items-center justify-center gap-2 mx-auto hover:bg-slate-50 transition-colors shadow-xl">
              무료 체험 시작
              <Rocket className="w-5 h-5 text-indigo-600" />
            </button>
            <p className="mt-4 text-sm text-indigo-200">
              신용카드 필요 없음
            </p>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white pt-16 pb-8 px-4 sm:px-6 lg:px-8 border-t border-slate-100">
        <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8 mb-12">
          <div className="col-span-2 lg:col-span-2">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">W</span>
              </div>
              <span className="font-bold text-xl tracking-tight">WriteFlow</span>
            </div>
            <p className="text-slate-500 max-w-sm">
              AI 기반의 차세대 글쓰기 도구.<br />
              상상을 현실의 문장으로.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-6">제품</h4>
            <ul className="space-y-4 text-slate-500 text-sm">
              <li><a href="#" className="hover:text-indigo-600">기능</a></li>
              <li><a href="#" className="hover:text-indigo-600">통합</a></li>
              <li><a href="#" className="hover:text-indigo-600">요금제</a></li>
              <li><a href="#" className="hover:text-indigo-600">로드맵</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-6">리소스</h4>
            <ul className="space-y-4 text-slate-500 text-sm">
              <li><a href="#" className="hover:text-indigo-600">블로그</a></li>
              <li><a href="#" className="hover:text-indigo-600">커뮤니티</a></li>
              <li><a href="#" className="hover:text-indigo-600">도움말 센터</a></li>
              <li><a href="#" className="hover:text-indigo-600">API 문서</a></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-6">회사</h4>
            <ul className="space-y-4 text-slate-500 text-sm">
              <li><a href="#" className="hover:text-indigo-600">소개</a></li>
              <li><a href="#" className="hover:text-indigo-600">채용</a></li>
              <li><a href="#" className="hover:text-indigo-600">개인정보처리방침</a></li>
              <li><a href="#" className="hover:text-indigo-600">이용약관</a></li>
            </ul>
          </div>
        </div>

        <div className="max-w-7xl mx-auto pt-8 border-t border-slate-100 flex flex-col md:flex-row items-center justify-between text-sm text-slate-500">
          <p>© 2024 WriteFlow Inc. All rights reserved.</p>
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            <a href="#" className="hover:text-slate-900">Twitter</a>
            <a href="#" className="hover:text-slate-900">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
