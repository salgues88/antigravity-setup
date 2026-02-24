import { login, signup } from './actions'
import Link from 'next/link'

export default async function LoginPage({
    searchParams,
}: {
    searchParams: Promise<{ message?: string; mode?: string }>
}) {
    const params = await searchParams
    const isSignup = params.mode === 'signup'
    const message = params.message

    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-[#111827] text-white py-12 px-4 sm:px-6 lg:px-8">
            {/* DevBlog Logo/Header (Top left in design) */}
            <div className="absolute top-6 left-6 flex items-center space-x-2">
                <div className="h-8 w-8 bg-blue-600 rounded-md rotate-45 flex items-center justify-center">
                    <div className="h-3 w-3 bg-white rounded-sm -rotate-45" />
                </div>
                <span className="text-xl font-bold tracking-tight">DevBlog</span>
            </div>

            <div className="w-full max-w-md space-y-8">
                <div className="text-center">
                    <h2 className="mt-6 text-3xl font-bold tracking-tight text-white">
                        {isSignup ? 'Create an account' : 'Welcome back'}
                    </h2>
                    <p className="mt-2 text-sm text-gray-400">
                        {isSignup
                            ? 'Sign up to access your developer dashboard.'
                            : 'Sign in to access your developer dashboard.'}
                    </p>
                </div>

                {message && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 px-4 py-3 rounded-md text-sm text-center">
                        {message}
                    </div>
                )}

                <form className="mt-8 space-y-6">
                    <div className="space-y-4">
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-300">
                                Email address
                            </label>
                            <div className="mt-1">
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    className="block w-full appearance-none rounded-md border border-gray-600 bg-gray-800/50 px-3 py-2 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
                                    placeholder="your@email.com"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between">
                                <label htmlFor="password" className="block text-sm font-medium text-gray-300">
                                    Password
                                </label>
                                {!isSignup && (
                                    <div className="text-sm">
                                        <a href="#" className="font-medium text-blue-500 hover:text-blue-400">
                                            Forgot password?
                                        </a>
                                    </div>
                                )}
                            </div>
                            <div className="mt-1 relative">
                                <input
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete={isSignup ? 'new-password' : 'current-password'}
                                    required
                                    className="block w-full appearance-none rounded-md border border-gray-600 bg-gray-800/50 px-3 py-2 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-blue-500 sm:text-sm"
                                    placeholder="Enter your password"
                                />
                                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                                    <svg className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div>
                        <button
                            formAction={isSignup ? signup : login}
                            className="flex w-full justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900"
                        >
                            {isSignup ? 'Sign Up' : 'Sign In'}
                        </button>
                    </div>
                </form>

                <div className="text-center text-sm text-gray-400">
                    {isSignup ? (
                        <>
                            Already have an account?{' '}
                            <Link href="/login" className="font-medium text-blue-500 hover:text-blue-400">
                                Sign in
                            </Link>
                        </>
                    ) : (
                        <>
                            Don't have an account?{' '}
                            <Link href="/login?mode=signup" className="font-medium text-blue-500 hover:text-blue-400">
                                Sign up
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}
