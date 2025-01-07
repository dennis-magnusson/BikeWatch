import { X } from "lucide-react";
import * as React from "react";

import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

type KeywordAdderProps = {
    keywords: string[];
    setKeywords: React.Dispatch<React.SetStateAction<string[]>>;
};

function KeywordAdder({ keywords, setKeywords }: KeywordAdderProps) {
    const [inputValue, setInputValue] = React.useState("");

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value);
    };

    const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter" && inputValue.trim() !== "") {
            e.preventDefault();
            addKeyword(inputValue.trim());
        }
    };

    const addKeyword = (keyword: string) => {
        if (!keywords.includes(keyword)) {
            setKeywords([...keywords, keyword]);
            setInputValue("");
        }
    };

    const removeKeyword = (keywordToRemove: string) => {
        setKeywords(keywords.filter((keyword) => keyword !== keywordToRemove));
    };

    return (
        <div className="flex flex-col gap-2 w-full max-w-sm">
            <div className="flex flex-wrap gap-2 min-h-[2.5rem] p-2 bg-background border rounded-md">
                {keywords.map((keyword) => (
                    <Badge
                        key={keyword}
                        variant="secondary"
                        className="text-sm"
                    >
                        {keyword}
                        <Button
                            variant="ghost"
                            size="sm"
                            className="ml-1 h-auto p-0 text-muted-foreground hover:text-foreground"
                            style={{ backgroundColor: "transparent" }}
                            onClick={() => removeKeyword(keyword)}
                        >
                            <X className="h-3 w-3" />
                            <span className="sr-only">Remove {keyword}</span>
                        </Button>
                    </Badge>
                ))}
                <Input
                    type="text"
                    value={inputValue}
                    onChange={handleInputChange}
                    onKeyDown={handleInputKeyDown}
                    className="flex-grow border-none shadow-none focus-visible:ring-0 focus-visible:ring-offset-0"
                    placeholder={
                        keywords.length === 0 ? "eg. Ultegra, Trek" : ""
                    }
                />
            </div>
            <p className="text-sm text-muted-foreground">
                Press Enter to add a keyword
            </p>
        </div>
    );
}

export default KeywordAdder;
