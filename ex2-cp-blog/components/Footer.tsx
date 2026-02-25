export default function Footer() {
    return (
        <footer className="border-t border-gray-200 bg-white py-8 mt-12">
            <div className="mx-auto max-w-5xl px-4 text-center sm:px-6 lg:px-8">
                <p className="text-sm text-gray-500">
                    © {new Date().getFullYear()} Antigravity. All rights reserved.
                </p>
            </div>
        </footer>
    );
}
