module Main where
import qualified Data.Char       as Char
import           Text.Regex.TDFA (AllTextMatches (getAllTextMatches), (=~))

main :: IO ()
main = do
    content <- readFile "../input.txt"
    let part1 = sum $ fmap calibrationValue (lines content)
    let part2 = sum $ fmap spelledCalibrationValue (lines content)
    print part1
    print part2

calibrationValue :: String -> Int
calibrationValue line = firstAndLastDigit digits
    where digits = filter Char.isDigit line

spelledCalibrationValue :: String -> Int
spelledCalibrationValue line = firstAndLastDigit digits
    where  digits = textMatchToCharNumber <$> getAllTextMatches (line =~ "one|two|three|four|five|six|seven|eight|nine|[1-9]")

firstAndLastDigit :: String -> Int
firstAndLastDigit digits = read [firstDigit, lastDigit]
    where firstDigit = head digits
          lastDigit = last digits

textMatchToCharNumber :: String -> Char
textMatchToCharNumber "one"   = '1'
textMatchToCharNumber "two"   = '2'
textMatchToCharNumber "three" = '3'
textMatchToCharNumber "four"  = '4'
textMatchToCharNumber "five"  = '5'
textMatchToCharNumber "six"   = '6'
textMatchToCharNumber "seven" = '7'
textMatchToCharNumber "eight" = '8'
textMatchToCharNumber "nine"  = '9'
textMatchToCharNumber x       = head x
