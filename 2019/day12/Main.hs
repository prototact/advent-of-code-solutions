module Main where

import Data.List (foldl', minimumBy)
import qualified Data.Map as M

newtype Planet = Planet (Int, Int, Int) deriving (Eq, Show)
newtype Velocity = Vel (Int, Int, Int) deriving Eq
newtype Accel = Accel (Int, Int, Int) deriving Show

data Dim = X | Y | Z deriving Eq

data Vector = Pl Planet | Vl Velocity | Ac Accel

enumerate :: Foldable t => t a -> [(Int, a)]
enumerate xs = let (_, ys) = foldl' comb (0, []) xs in reverse ys
    where 
        comb (cnt, zs) x = (cnt + 1, (cnt, x):zs)

projx :: Vector -> Int
projx (Pl (Planet (x,_,_))) = x
projx (Vl (Vel (x,_,_))) = x
projx (Ac (Accel (x,_,_))) = x

projy :: Vector -> Int
projy (Pl (Planet (_,y,_))) = y
projy (Vl (Vel (_,y,_))) = y
projy (Ac (Accel (_,y,_))) = y

projz :: Vector -> Int
projz (Pl (Planet (_,_,z))) = z
projz (Vl (Vel (_,_,z))) = z
projz (Ac (Accel (_,_,z))) = z

pair :: [Planet] -> [((Int, Planet), (Int, Planet))]
pair planets = go enumerated
    where
        enumerated = enumerate planets 
        go [] = []
        go (planet:planets) = map (planet,) planets ++ go planets


evolve :: [Planet] -> [Velocity] -> [Accel] -> (Int, Int, Int, [Planet], [Velocity])
evolve planets velocities accels = (p1, p2, t, locations, newVelocities)
    where
        solve dim p q x x' = ceiling ((-beta + sqrt delta) / (2.0 * alpha))
            where
                v p
                    | dim == X = let Vel (vx, _, _) = velocities !! p in vx
                    | dim == Y = let Vel (_, vy, _) = velocities !! p in vy
                    | otherwise = let Vel (_, _, vz) = velocities !! p in vz
                ac p
                    | dim == X = let Accel (ax, _, _) = accels !! p in ax
                    | dim == Y = let Accel (_, ay, _) = accels !! p in ay
                    | otherwise = let Accel (_, _, az) = accels !! p in az
                alpha = fromIntegral (ac p - ac q) / 2.0
                beta = fromIntegral (2 * v p + ac p - 2 * v q - ac q) / 2
                gamma = fromIntegral (x - x')
                delta = beta * beta - 4.0 * alpha * gamma
        findRoot (p, Planet (x, y, z)) (q, Planet (x', y', z')) = minimum [solve X p q x x', solve Y p q y y', solve Z p q z z']
        (p1, p2, t) = minimumBy (\(_, _, tau) (_, _, tau') -> compare tau tau') . map (\((p, planet), (q, other)) -> (p, q, findRoot (p, planet) (q, other))) $ pair planets
        stepLoc vel accel = vel * t + accel * div (t * (t + 1)) 2
        applyVec f (Planet (x, y, z)) (Vel (vx, vy, vz)) (Accel (ax, ay, az)) = Planet (x + f vx ax, y + f vy ay, z + f vz az)
        locations = zipWith3 (applyVec stepLoc) planets velocities accels
        stepVec (Vel (vx, vy, vz)) (Accel (ax, ay, az)) = Vel (vx + ax * t, vy + ay * t, vz + az * t)
        newVelocities = zipWith stepVec velocities accels

stepLarge :: [Planet] -> [Velocity] -> [Accel] -> ([Planet], [Velocity], [Accel])
stepLarge planets velocities accels = (locations, newVelocities, newAccels)
    where
        (p, q, t, locations, newVelocities) = evolve planets velocities accels
        newAccels = undefined  -- i have to update the accels vector by changing the p and q items by + 1, - 1, if vp > 0 and vq < 0
        -- the issue is i need to step one more time for the two to move. but what if they stay still, or two other planets meet at dim? crap


computeAccels :: [Planet] -> [Accel]
computeAccels planets = let pairs = pair planets in let accelsMap = foldr comb M.empty pairs in map snd $ M.toList accelsMap
    where 
        comb ((left, planet), (right, other)) accels = M.alter (updateAccel other planet) right $ M.alter (updateAccel planet other) left accels
        updateAccel planet other Nothing = Just (Accel (accel projx (planet, other), accel projy (planet, other), accel projz (planet, other)))
        updateAccel planet other (Just (Accel (x, y, z))) = Just (Accel (x + accel projx (planet, other), y + accel projy (planet, other), z + accel projz (planet, other)))
        accel proj (planet, other)
            | proj (Pl planet) < proj (Pl other) = 1 
            | proj (Pl planet) == proj (Pl other) = 0
            | otherwise = -1

computeStep :: Vector -> Vector -> Vector
computeStep = move
    where 
        move v@(Vl _) ac@(Ac _) = Vl (Vel (projx v + projx ac, projy v + projy ac, projz v + projz ac))
        move loc@(Pl _) v@(Vl _) = Pl (Planet (projx loc + projx v, projy loc + projy v, projz loc + projz v))
        move _ _ = error "unexpected call"

step :: (Integer, [Planet], [Velocity]) -> (Integer, [Planet], [Velocity])
step (cnt, planets, velocities) = (cnt + 1, locations, newVelocities)
    where
        accels = computeAccels planets
        newVelocities = map (\(Vl v) -> v) . zipWith computeStep (map Vl velocities) $ map Ac accels
        locations = map (\(Pl loc) -> loc) . zipWith computeStep (map Pl planets) $ map Vl newVelocities

run :: [Planet] -> Integer
run planets = let (cnt, _, _) = until (\(cnt, pl, vl) -> cnt > 1 && pl == planets && vl == velocities) step (0, planets, velocities) in cnt
    where
        velocities = map (\_ -> Vel (0, 0, 0)) planets

main :: IO ()
main = do
    let planets = [Planet (-1, 0, 2), Planet (2, -10, -7), Planet (4, -8, 8), Planet (3, 5, -1)]
    print $ run planets
    let planets = [Planet (8, -10, 0), Planet (5, 5, 10), Planet (2, -7, 3), Planet  (9, -8, -3)]
    print $ run planets  -- takes practically forever