import {
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
} from "./ui/pagination";

interface PaginationBarProps {
    totalPages: number;
    page: number;
    handlePageChange: (page: number) => void;
}

export function PaginationBar({
    totalPages,
    page,
    handlePageChange,
}: PaginationBarProps) {
    const handlePageClick = (newPage: number) => {
        handlePageChange(newPage);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const renderPaginationItems = () => {
        const items = [];
        const maxDisplayedPages = 5;
        const halfMaxDisplayedPages = Math.floor(maxDisplayedPages / 2);

        if (totalPages <= maxDisplayedPages) {
            for (let i = 1; i <= totalPages; i++) {
                items.push(
                    <PaginationItem key={i}>
                        <PaginationLink
                            href="#"
                            onClick={() => handlePageClick(i)}
                            isActive={page === i}
                            size="icon"
                        >
                            {i}
                        </PaginationLink>
                    </PaginationItem>
                );
            }
        } else {
            items.push(
                <PaginationItem key={1}>
                    <PaginationLink
                        href="#"
                        onClick={() => handlePageClick(1)}
                        isActive={page === 1}
                        size="icon"
                    >
                        1
                    </PaginationLink>
                </PaginationItem>
            );

            if (page > halfMaxDisplayedPages + 2) {
                items.push(<PaginationEllipsis key="ellipsis1" />);
            }

            const startPage = Math.max(2, page - halfMaxDisplayedPages);
            const endPage = Math.min(
                totalPages - 1,
                page + halfMaxDisplayedPages
            );

            for (let i = startPage; i <= endPage; i++) {
                items.push(
                    <PaginationItem key={i}>
                        <PaginationLink
                            href="#"
                            onClick={() => handlePageClick(i)}
                            isActive={page === i}
                            size="icon"
                        >
                            {i}
                        </PaginationLink>
                    </PaginationItem>
                );
            }

            if (page < totalPages - halfMaxDisplayedPages - 1) {
                items.push(<PaginationEllipsis key="ellipsis2" />);
            }

            items.push(
                <PaginationItem key={totalPages}>
                    <PaginationLink
                        href="#"
                        onClick={() => handlePageClick(totalPages)}
                        isActive={page === totalPages}
                        size="icon"
                    >
                        {totalPages}
                    </PaginationLink>
                </PaginationItem>
            );
        }

        return items;
    };

    return (
        <div className="w-full flex justify-center">
            <Pagination>
                <PaginationContent>
                    <PaginationItem>
                        <PaginationPrevious
                            onClick={() => handlePageClick(page - 1)}
                            size="default"
                        />
                    </PaginationItem>
                    {renderPaginationItems()}
                    <PaginationItem>
                        <PaginationNext
                            onClick={() => handlePageClick(page + 1)}
                            size="default"
                        />
                    </PaginationItem>
                </PaginationContent>
            </Pagination>
        </div>
    );
}
