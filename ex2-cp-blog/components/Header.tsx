import Link from "next/link";
import { User } from "@supabase/supabase-js";
import { logout } from "@/app/login/actions";

export default function Header({ user }: { user: User | null }) {
    return (
        <header className="border-b border-gray-200 bg-white">
            <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6 lg:px-8">
                <div className="flex items-center">
                    <Link href="/" className="text-xl font-bold tracking-tighter text-black">
                        Antigravity blog
                    </Link>
                </div>
                <div className="flex items-center gap-4">
                    {user ? (
                        <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-600">{user.email}</span>
                            <form action={logout}>
                                <button
                                    type="submit"
                                    className="text-sm font-medium text-red-600 hover:text-red-800 transition-colors"
                                >
                                    로그아웃
                                </button>
                            </form>
                        </div>
                    ) : (
                        <Link
                            href="/login"
                            className="text-sm font-medium text-gray-700 hover:text-black transition-colors"
                        >
                            로그인
                        </Link>
                    )}
                </div>
            </div>
        </header>
    );
}
