module Main where

import Control.Exception (assert)
import Data.Char (isDigit, isPunctuation, isSpace)
import Data.List (break, intercalate, nub, splitAt, uncons, unlines)

data Spring = Okay | Broken | Wildcard deriving (Show, Eq)

type Springrows = [([Spring], [Int])]

breakOn :: (Char -> Bool) -> String -> (String, Maybe String)
breakOn pred xs = actual
  where
    (start, rest) = break pred xs
    actual = case uncons rest of
        Nothing -> (start, Nothing)
        Just (x, xs) -> (start, Just xs)

splitNumbers :: String -> [Int]
splitNumbers = reverse . go []
  where
    go acc [] = acc
    go acc xs = case breakOn isPunctuation xs of
        (number, Nothing) -> read number : acc
        (number, Just xs) -> go (read number : acc) xs

parseSprings :: String -> [Spring]
parseSprings = map spring
  where
    spring '.' = Okay
    spring '#' = Broken
    spring '?' = Wildcard

parseSpringRows :: String -> Springrows
parseSpringRows file = do
    line <- lines file
    let (springs, sizes) = case breakOn isSpace line of
            (spr, Nothing) -> (spr, [])
            (spr, Just xs) -> (spr, xs)
    return (parseSprings springs, splitNumbers sizes)

breakGroups :: [Spring] -> [[Spring]]
breakGroups = reverse . filter (not . null) . map reverse . go []
  where
    go acc [] = acc
    go [] (x : xs) = if x /= Okay then go [[x]] xs else go [] xs
    go (group : groups) (x : xs) = if x /= Okay then go ((x : group) : groups) xs else go ([] : group : groups) xs

multiplyBy5 :: [Spring] -> [Int] -> ([Spring], [Int])
multiplyBy5 springs sizes = (springs5, sizes5)
  where
    springs5 = (intercalate [Wildcard] . replicate 5) springs
    sizes5 = concat . replicate 5 $ sizes

countOrderings :: [[Spring]] -> [Int] -> Int
countOrderings groups [] = if all (notElem Broken) groups then 1 else 0
countOrderings [] (_ : _) = 0
countOrderings (group : groups) (size : sizes)
    | length group < size = if all (== Wildcard) group then countOrderings groups (size : sizes) else 0
    | length group == size = countOrderings groups sizes + if all (== Wildcard) group then countOrderings groups (size : sizes) else 0
    | otherwise = alignSizes size group + if all (== Wildcard) group then countOrderings groups (size : sizes) else 0
  where
    alignSizes :: Int -> [Spring] -> Int
    alignSizes size xs = sum [countMore (split idx) | idx <- [0 .. length xs - size]]
      where
        split idx = let (start, rest) = splitAt idx xs in let (_, end) = splitAt size rest in (start, end)
        countMore (start, []) = if all (== Wildcard) start then countOrderings groups sizes else 0
        countMore (start, x : xs) = if all (== Wildcard) start && x == Wildcard then countOrderings (xs : groups) sizes else 0

count :: [Spring] -> [Int]
count = filter (/= 0) . go
  where
    go [] = [0]
    go (Broken : xs) = let (c : cs) = go xs in (c + 1 : cs)
    go (Okay : xs) = 0 : go xs
    go (Wildcard : xs) = go xs

match' :: [Int] -> [Int] -> Bool
match' _ [] = True
match' sizes xs = let ((x, y) : zs) = reverse (zip xs sizes) in all (uncurry (==)) zs && x <= y

fill :: [Int] -> [Spring] -> [[Spring]]
fill sizes = go
  where
    go [] = [[]]
    go (Wildcard : xs) =
        [ x : zs | x <- [Okay, Broken], zs <- go xs, let start = count . reverse $ (x : zs), match' sizes start
        ]
    go (Broken : xs) = filter (\x -> let start = count . reverse $ x in match' sizes start) . map (Broken :) . go $ xs
    go (Okay : xs) = error "should never occur"

countOrderings' :: [[Spring]] -> [Int] -> Int
countOrderings' [] sizes = if not . null $ sizes then 0 else 1
countOrderings' groups [] = if all (all (== Wildcard)) groups then 1 else 0
countOrderings' (group : groups) sizes = sum [countOrderings' groups (drop (length matched) sizes) | matched <- getMatches group]
  where
    match :: [Int] -> Bool
    match x = (length x <= length sizes) && (and . zipWith (==) sizes $ x)
    getMatches :: [Spring] -> [[Int]]
    getMatches = filter match . map (count . reverse) . fill sizes . reverse

main :: IO ()
main = do
    file <- readFile "sample.txt"
    let springrows = parseSpringRows file
    let filled = filter (and . zipWith (==) [3, 2, 1]) . map (count . reverse) . fill [3, 2, 1] . reverse . parseSprings $ "?###????????"
    let grouped = map (\(group, sizes) -> (breakGroups group, sizes)) springrows
    let expected = map (uncurry countOrderings') grouped
    print expected
    print $ assert (sum expected == 21) "small test ok!"
    let multiplied = map (uncurry multiplyBy5) springrows
    let grouped = map (\(group, sizes) -> (breakGroups group, sizes)) multiplied
    print $ assert (sum (map (uncurry countOrderings') grouped) == 525152) "count ok!"
    -- test over
    file <- readFile "input.txt"
    let springrows = parseSpringRows file
    let multiplied = map (uncurry multiplyBy5) springrows
    let grouped = map (\(group, sizes) -> (breakGroups group, sizes)) multiplied
    print $ sum (map (uncurry countOrderings') grouped)