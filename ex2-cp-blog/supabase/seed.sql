-- Seed data for categories
INSERT INTO public.categories (id, name) VALUES
    ('11111111-1111-1111-1111-111111111111', 'React'),
    ('22222222-2222-2222-2222-222222222222', 'Next.js'),
    ('33333333-3333-3333-3333-333333333333', 'Supabase'),
    ('44444444-4444-4444-4444-444444444444', 'Tailwind CSS')
ON CONFLICT (name) DO NOTHING;

-- Seed data for posts (dummy posts)
INSERT INTO public.posts (id, title, summary, content, category_id, image_url, created_at) VALUES
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        'Next.js 14 App Router 시작하기',
        'Next.js 14의 App Router를 사용하여 강력한 웹 애플리케이션을 구축하는 방법을 알아봅니다.',
        '본문 내용입니다...',
        '22222222-2222-2222-2222-222222222222', -- Next.js
        'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=2670&auto=format&fit=crop',
        now() - INTERVAL '1 days'
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        'Supabase와 Next.js 연동 가이드',
        '오픈소스 파이어베이스 대안인 Supabase를 Next.js 프로젝트에 통합하고 데이터를 관리해봅시다.',
        '본문 내용입니다...',
        '33333333-3333-3333-3333-333333333333', -- Supabase
        'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2670&auto=format&fit=crop',
        now() - INTERVAL '2 days'
    ),
    (
        'cccccccc-cccc-cccc-cccc-cccccccccccc',
        'Tailwind CSS로 빠른 스타일링',
        '유틸리티 퍼스트 CSS 프레임워크인 Tailwind CSS를 사용해 현대적인 UI를 빠르게 구축하세요.',
        '본문 내용입니다...',
        '44444444-4444-4444-4444-444444444444', -- Tailwind CSS
        'https://images.unsplash.com/photo-1507721999472-8ed4421c4af2?q=80&w=2670&auto=format&fit=crop',
        now() - INTERVAL '3 days'
    ),
    (
        'dddddddd-dddd-dddd-dddd-dddddddddddd',
        'React 서버 컴포넌트의 이해',
        'React 18부터 도입된 서버 컴포넌트의 개념과 장점, 그리고 사용 방법에 대해 깊이 알아봅니다.',
        '본문 내용입니다...',
        '11111111-1111-1111-1111-111111111111', -- React
        'https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=2670&auto=format&fit=crop',
        now() - INTERVAL '4 days'
    ),
    (
        'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
        '프론트엔드 개발자 로드맵 2024',
        '성공적인 프론트엔드 개발자가 되기 위해 필요한 핵심 기술과 학습 경로를 안내합니다.',
        '본문 내용입니다...',
        '11111111-1111-1111-1111-111111111111', -- React
        'https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=2672&auto=format&fit=crop',
        now() - INTERVAL '5 days'
    ),
    (
        'ffffffff-ffff-ffff-ffff-ffffffffffff',
        '데이터베이스 모델링 필수 가이드',
        '안정적이고 확장 가능한 백엔드 시스템을 위한 관계형 데이터베이스 모델링 기초.',
        '본문 내용입니다...',
        '33333333-3333-3333-3333-333333333333', -- Supabase
        'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?q=80&w=2612&auto=format&fit=crop',
        now() - INTERVAL '6 days'
    )
ON CONFLICT (id) DO NOTHING;
