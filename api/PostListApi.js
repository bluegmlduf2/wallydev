import BaseApi from './BaseApi'

class PostListApi extends BaseApi {
  /**
   * The constructor for the ArtistApi.
   *
   * @param {Object} parameters The query parameters.
   */
  constructor(parameters = {}) {
    // BaseApi.js의 부모의 constructor를 실행, 부모의 endpoint는 reclist사용
    super('api_wallydev/post/postlist', parameters)
  }

  /**
   * 게시물 가져오기
   */
  getPostList({ searchText, category, page }) {
    const params = { page, limit: '12' }

    // 검색어조건이 있는 경우와 없는 경우
    if (searchText) {
      params.q = searchText
    } else {
      params.category = category
    }

    // 게시물을 12개씩 가져온다
    this.setParameters(params)
    return this.all()
  }
}

export default PostListApi
