# actions-private-actions

This action enables the use of custom actions in private repos.

Actions, [by default](https://docs.github.com/en/actions/creating-actions/about-custom-actions#choosing-a-location-for-your-action), must be in public repos to be usable by other repos. One way around this, is to check actions out into the `.github/actions/action-name` directory.  That's what this action does.

# Using this action

```
- uses: junipersquare/actions-private-actions@main
  with:
    repo-list: '["junipersquare/actions-some-private-action@main", "junipersquare/actions-some-other-action@main"]'
    token: ${{secrets.SOME_GITHUB_PAT}}
```
