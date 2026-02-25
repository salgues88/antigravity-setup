import { Category } from "@/types/supabase";

type CategoryFilterProps = {
    categories: Category[];
    selectedCategoryId: string | null;
    onSelectCategory: (id: string | null) => void;
};

export default function CategoryFilter({
    categories,
    selectedCategoryId,
    onSelectCategory,
}: CategoryFilterProps) {
    return (
        <div className="mb-8 flex flex-wrap gap-2">
            <button
                onClick={() => onSelectCategory(null)}
                className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${selectedCategoryId === null
                        ? "bg-black text-white"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                    }`}
            >
                All
            </button>
            {categories.map((category) => (
                <button
                    key={category.id}
                    onClick={() => onSelectCategory(category.id)}
                    className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${selectedCategoryId === category.id
                            ? "bg-black text-white"
                            : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                        }`}
                >
                    {category.name}
                </button>
            ))}
        </div>
    );
}
