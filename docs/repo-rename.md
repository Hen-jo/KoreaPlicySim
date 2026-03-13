# Repo Rename Notes

The runtime and product identity now use `KoreaPolicySim`, but the repository and local folder may still be named `MiroFish` until the move is completed.

## Planned Steps

1. Create the new GitHub repository slug, for example `666ghj/KoreaPolicySim`.
2. Rename the local workspace folder from `/Users/jo/miro/MiroFish` to `/Users/jo/miro/KoreaPolicySim`.
3. Update the local git remote:

```bash
git remote set-url origin https://github.com/666ghj/KoreaPolicySim.git
```

4. Update any CI/CD variables, package registry image names, and deployment scripts that still reference `MiroFish` or `mirofish`.
5. Regenerate badges, screenshots, and brand assets later if you want the file names and media labels to match the new product name exactly.
